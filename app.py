from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serves index.html

@app.route('/generate_table', methods=['GET'])
def generate_table():
    table_name = request.args.get('table_name')  # Get table_name from query parameters
    if not table_name:
        return jsonify({"error": "Missing table_name parameter"}), 400

    # Connect to SQLite database
    conn = sqlite3.connect("usccb_project.db")
    cursor = conn.cursor()

    # Query the database
    cursor.execute(f"""
    SELECT {table_name}.paragraph, Vatican.ccc_number, Vatican.paragraph
    FROM {table_name}
    INNER JOIN Vatican ON {table_name}.ccc_number = Vatican.ccc_number
    """)

    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    # Generate HTML table output
    html_table = """
    <table id="myTable" border='1'>
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
