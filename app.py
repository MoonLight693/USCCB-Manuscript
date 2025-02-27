from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serves index.html

@app.route('/generate_table', methods=['GET'])
def generate_table():
    # Connect to SQLite database
    conn = sqlite3.connect("usccb_project.db")
    cursor = conn.cursor()

    # Query the database
    table_name = "your_table_name"
    cursor.execute("""
    SELECT Jesus_2.paragraph, Vatican.ccc_number, Vatican.paragraph
    FROM Jesus_2
    INNER JOIN Vatican ON Jesus_2.ccc_number = Vatican.ccc_number
    """)

    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    # Generate HTML table output
    html_table = """
    <table border='1'>
        <tr>{}</tr>
        {}
    </table>
    """.format(
        "".join(f"<th>{col}</th>" for col in columns),
        "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    )

    conn.close()
    
    return jsonify({"table": html_table})

if __name__ == '__main__':
    app.run(debug=True)
