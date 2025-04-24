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
from force_highlight import highlight_multiline_quotes  # Import the highlight_sentences function

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
DB_FILE = os.getenv("DB_NAME")


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS files (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT UNIQUE,
                            original_filepath TEXT,
                            highlighted_filepath TEXT,
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
            cursor = conn.execute("INSERT INTO files (filename, original_filepath, highlighted_filepath, status, date_submitted) VALUES (?, ?, ?, ?, ?)",
                                  (file.filename, file_path, None, 'Ready for Review', date_submitted))
            file_id = cursor.lastrowid

        # Emit the status update for Socket.IO
        socketio.emit('status_update', {'id': file_id, 'status': 'Ready For Review'})

        # Run AI_State_Machine.py
        try:
            subprocess.run(
                ["python3", "AI_State_Machine.py"],  # Updated to relative path
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
                ["python3", "convert.py"],  # Updated to relative path
                check=True
            )
            print("✅ convert.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing convert.py: {e}")
            flash("Error converting the file into the database.", 'error')
            return redirect(url_for('index'))

        # Fetch paragraphs from the newly created table and highlight them
        try:
            table_name = file.filename.replace('.pdf', '').replace(' ', '_').replace('-', '_')  # Replace dashes with underscores
            sentences_to_highlight = []
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT paragraph FROM {table_name}")
                sentences_to_highlight = [row[0].strip() for row in cursor.fetchall()]  # Strip whitespace
                print(f"🔍 Sentences to highlight: {sentences_to_highlight}")  # Debugging log

            if sentences_to_highlight:
                highlighted_file_path = file_path.replace('.pdf', '_highlighted.pdf')
                highlight_multiline_quotes(file_path, highlighted_file_path, sentences_to_highlight)
                print("✅ Sentences highlighted successfully.")

                # Update the database with the highlighted file path
                with sqlite3.connect(DB_FILE) as conn:
                    conn.execute("UPDATE files SET highlighted_filepath = ? WHERE id = ?", (highlighted_file_path, file_id))
                    conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error fetching paragraphs for highlighting: {e}")
            flash("Error highlighting sentences in the PDF.", 'error')
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
        conn.row_factory = sqlite3.Row  # Ensure rows are returned as dictionary-like objects
        file = conn.execute("SELECT original_filepath, highlighted_filepath, filename FROM files WHERE id = ?", (file_id,)).fetchone()
    
    if not file:
        return redirect(url_for('index'))  # Redirect to 'index' if file not found

    # Use highlighted file if available, otherwise fallback to original file
    file_path = file['highlighted_filepath'] if file['highlighted_filepath'] else file['original_filepath']
    table_name = file['filename'].replace('.pdf', '').replace(' ', '_').replace('-', '_')  # Use original filename for table name
    html_table = ""

    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Check if the table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                flash(f"Table '{table_name}' does not exist.", 'error')
                return redirect(url_for('index'))

            # Query the table
            cursor.execute(f'''
            SELECT {table_name}.paragraph, Vatican.reference, Vatican.paragraph
            FROM {table_name}
            INNER JOIN Vatican ON {table_name}.reference = Vatican.reference
            ''')
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
        
        html_table = f"""
        <table id='myTable' border='1'>
            <tr>{''.join(f'<th>{col}</th>' for col in columns)}</tr>
            {''.join('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>' for row in rows)}
        </table>
        """
    except sqlite3.Error as e:
        flash(f"Database error: {e}", 'error')
        return redirect(url_for('index'))

    return render_template('pdfjs_viewer.html', filename=os.path.basename(file_path), file_id=file_id, table=html_table, table_name=table_name)

# File Deletion Route
@app.route('/delete/<int:file_id>', methods=['POST'])
def delete(file_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row  # Ensure rows are returned as dictionary-like objects
        file = conn.execute("SELECT original_filepath, highlighted_filepath, filename FROM files WHERE id = ?", (file_id,)).fetchone()
        if file:
            # Remove the original file
            if file['original_filepath'] and os.path.exists(file['original_filepath']):
                os.remove(file['original_filepath'])
            
            # Remove the highlighted file
            if file['highlighted_filepath'] and os.path.exists(file['highlighted_filepath']):
                os.remove(file['highlighted_filepath'])
            
            # Sanitize the table name by replacing spaces and dashes with underscores
            table_name = file['filename'].replace('.pdf', '').replace(' ', '_').replace('-', '_')
            try:
                conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            except sqlite3.Error as e:
                print(f"❌ Error dropping table {table_name}: {e}")
            
            # Delete the file record from the database
            conn.execute("DELETE FROM files WHERE id = ?", (file_id,))
            conn.commit()
    
    # Emit the status update for Socket.IO
    socketio.emit('status_update', {'id': file_id, 'status': 'deleted'})
    flash("File and associated data deleted successfully!", 'success')
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

    def normalize_book_name(book_raw):
        """Normalize book name to match USCCB URL format."""
        book = book_raw.strip().lower().replace(" ", "")
        replacements = {
            'songofsongs': 'songofsongs',
            'song of songs': 'songofsongs',
            'songs': 'songofsongs',
        }
        return replacements.get(book, book)

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name.replace('-', '_'),))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': f'Table \"{table_name}\" does not exist'}), 404

            cursor.execute(f"SELECT paragraph, reference FROM {table_name.replace('-', '_')}")
            rows = cursor.fetchall()

        html_table = f"""
        <div class='table-responsive'>
            <table class='table table-bordered table-hover' id='myTable'>
                <thead>
                    <tr>
                        <th>Verify</th>
                        <th>Paragraph</th>
                        <th>Reference</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
        """
        for row in rows:
            paragraph, reference = row
            reference_link = ""
            if reference:
                try:
                    # Example reference: "Matthew 22:37-39" or "1 John 4:8"
                    parts = reference.split(":")
                    if len(parts) != 2:
                        raise ValueError("Invalid format")

                    book_and_chapter = parts[0].strip()  # e.g., "1 John 4"
                    verse = parts[1].split("-")[0].strip()  # use the start of a range if present

                    *book_parts, chapter = book_and_chapter.split()
                    book_name = ''.join(book_parts)
                    if book_parts and book_parts[0].isdigit():
                        book_name = book_parts[0] + ''.join(book_parts[1:])
                    book = normalize_book_name(book_name)

                    reference_link = f"https://bible.usccb.org/bible/{book}/{chapter}?{verse}="
                    reference = f'<a href="{reference_link}" target="_blank">{reference}</a>'
                except Exception as e:
                    print(f"Error parsing reference '{reference}': {e}")

            html_table += f"""
                <tr>
                    <td><input type="checkbox" name="row_select" value="{paragraph}"></td>
                    <td>{paragraph}</td>
                    <td>{reference}</td>
                    <td><input type="text" name="notes_{paragraph}" placeholder="Add notes"></td>
                </tr>
            """
        html_table += """
                </tbody>
            </table>
        </div>
        """

        return jsonify({'success': True, 'table': html_table})


    except sqlite3.Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True)
