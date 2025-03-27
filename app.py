from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, session, jsonify
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import os
import sqlite3
import secrets
from datetime import datetime
from dotenv import load_dotenv
from forms import LoginForm, RegisterForm, UploadForm
from threading import Lock
import subprocess  # Add subprocess to execute external scripts

# If multiple requests overlap (e.g., two requests attempt to overwrite the file simultaneously), SQLite may reject one.
# Introduce a lock to ensure only one active write per file.
save_lock = Lock()

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'USCCB Test Input Directory'

# Set the secret key for the session, using the .env file for better security
app.secret_key = os.getenv("SECRET_KEY") or secrets.token_hex(32)

# Initialize SocketIO and other extensions
socketio = SocketIO(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Database
DB_FILE = 'demo.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS files (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT UNIQUE,
                            filepath TEXT,
                            status TEXT,
                            date_submitted TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            display_name TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)''')

init_db()

# Database connection function
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This will return rows as dictionaries
    return conn

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with sqlite3.connect(DB_FILE) as conn:
        files = conn.execute("SELECT * FROM files ORDER BY filename ASC").fetchall()
    form = UploadForm()
    return render_template('upload.html', files=files, form=form)

# User Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        display_name = form.display_name.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, display_name, email, password) VALUES (?, ?, ?, ?)',
                     (username, display_name, email, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))  # Redirect to the index if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash("Invalid username or password")

    return render_template('login.html', form=form)

# User Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# PDF Upload Route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file selected", 'error')  # Flash an error message
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash("Empty filename", 'error')  # Flash an error message
        return redirect(url_for('index'))

    if file and file.filename.endswith('.pdf'):
        # Check if file already exists
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(file_path):
            flash("File already exists.", 'error')  # Flash an error message
            return redirect(url_for('index'))
        file.save(file_path)

        # Insert file details into the database
        date_submitted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.execute("INSERT INTO files (filename, filepath, status, date_submitted) VALUES (?, ?, ?, ?)",
                                  (file.filename, file_path, 'completed', date_submitted))
            file_id = cursor.lastrowid

        # Emit the status update for Socket.IO
        socketio.emit('status_update', {'id': file_id, 'status': 'completed'})

        # Run AI_State_Machine.py
        try:
            subprocess.run(
                ["python3", "/home/whitmercraft939/USCCB-Manuscript-3/AI_State_Machine.py"],
                check=True
            )
            print("✅ AI_State_Machine.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing AI_State_Machine.py: {e}")
            flash("Error processing the file with AI State Machine.", 'error')
            return redirect(url_for('index'))

        # Run convert.py
        try:
            subprocess.run(
                ["python3", "/home/whitmercraft939/USCCB-Manuscript-3/convert.py"],
                check=True
            )
            print("✅ convert.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing convert.py: {e}")
            flash("Error converting the file into the database.", 'error')
            return redirect(url_for('index'))

        flash("File uploaded and processed successfully!", 'success')  # Flash a success message
        return redirect(url_for('index'))

    flash("Invalid file type", 'error')  # Flash an error message
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/viewer/<int:file_id>', methods=['GET'])
def view_pdf(file_id):
    with sqlite3.connect(DB_FILE) as conn:
        file = conn.execute("SELECT filename FROM files WHERE id = ?", (file_id,)).fetchone()
    
    if not file:
        return redirect(url_for('index'))  # Fixed redirect to 'index' instead of 'home'
    
    table_name = request.args.get('table_name')
    html_table = ""
    if table_name:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            SELECT {table_name}.paragraph, Vatican.ccc_number, Vatican.paragraph
            FROM {table_name}
            INNER JOIN Vatican ON {table_name}.ccc_number = Vatican.ccc_number
            ''')
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
        
        html_table = f"""
        <table id='myTable' border='1'>
            <tr>{''.join(f'<th>{col}</th>' for col in columns)}</tr>
            {''.join('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>' for row in rows)}
        </table>
        """  # Fixed missing 'rows' variable in the loop

    return render_template('pdfjs_viewer.html', filename=file[0], file_id=file_id, table=html_table)

# File Deletion Route
@app.route('/delete/<int:file_id>', methods=['POST'])
def delete(file_id):
    with sqlite3.connect(DB_FILE) as conn:
        file = conn.execute("SELECT filepath FROM files WHERE id = ?", (file_id,)).fetchone()
        if file:
            os.remove(file[0])
            conn.execute("DELETE FROM files WHERE id = ?", (file_id,))
    socketio.emit('status_update', {'id': file_id, 'status': 'deleted'})
    flash("File deleted successfully!", 'success')
    return redirect(url_for('index'))

# File Status Update Route
@app.route('/update_status/<int:file_id>', methods=['POST'])
def update_status(file_id):
    new_status = request.form['status']
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("UPDATE files SET status = ? WHERE id = ?", (new_status, file_id))
        conn.commit()

    # Emit the status update for Socket.IO
    socketio.emit('status_update', {'id': file_id, 'status': new_status})

    flash("File status updated successfully!", 'success')
    return redirect(url_for('index'))

@app.route('/generate_table', methods=['GET'])
def generate_table():
    table_name = request.args.get('table_name')
    if not table_name:
        return jsonify({'success': False, 'message': 'Table name is required'}), 400

    # Replace spaces with underscores to match the database table naming convention
    table_name = table_name.replace(' ', '_')
    print(f"🔍 Received table name: {table_name}")  # Debugging log

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            # Check if the table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                print(f"❌ Table does not exist: {table_name}")  # Debugging log
                return jsonify({'success': False, 'message': f'Table "{table_name}" does not exist'}), 404

            # Query the table
            cursor.execute(f'''
            SELECT {table_name}.paragraph, Vatican.ccc_number, Vatican.paragraph
            FROM {table_name}
            INNER JOIN Vatican ON {table_name}.ccc_number = Vatican.ccc_number
            ''')
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()

        html_table = f"""
        <table id='myTable' border='1'>
            <tr>{''.join(f'<th>{col}</th>' for col in columns)}</tr>
            {''.join(f'<tr>{"".join(f"<td>{cell}</td>" for cell in row)}</tr>' for row in rows)}
        </table>
        """

        return jsonify({'success': True, 'table': html_table})

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")  # Debugging log
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, debug=True)
