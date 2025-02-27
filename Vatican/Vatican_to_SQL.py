'''
Author: Emma Hickey
Last Date Modified: Feb 5, 2025
Description: This script is creating a SQLite database and making an SQLite table pulled from the CCC_table.txt. 
Links to additional resources:
- https://www.geeksforgeeks.org/python-sqlite-create-table/
- https://www.youtube.com/watch?v=girsuXz0yA8
'''
import sqlite3

'''Josh's section--------------------------------------------------------------------------------'''
def to_table(path, table_name):
    '''give the file path to the txt and the name of the table you want created in the database'''
    # Connecting to sqlite 
    conn = sqlite3.connect("usccb_project.db")
    cursor = conn.cursor()
    
    #drop table if exist
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    #Create the CCC table
    cursor.execute(f'CREATE TABLE {table_name} (ccc_number txt, paragraph txt)')
    
    f = open(path, "r")
    for x in f:
        z = x.split("$")
        exe = f"insert into {table_name}(CCC_number, paragraph) values "
        cursor.execute(exe + '($1, $2)', z)
    
    #Commit changes and close connection 
    conn.commit()
    conn.close()
'''----------------------------------------------------------------------------------------------'''
    
def delete_table(table_name):
    '''deletes table of by name from the database if exists.'''
    # Connecting to sqlite 
    conn = sqlite3.connect("usccb_project.db")
    cursor = conn.cursor()
    #drop table if exist
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    #Commit changes and close connection 
    conn.commit()
    conn.close()

def reference_query():
    # Connect to SQLite database
    conn = sqlite3.connect("usccb_project.db")
    cursor = conn.cursor()

    # Query the database
    cursor.execute(f"""SELECT Jesus_2.paragraph, Vatican.ccc_number, Vatican.paragraph
                   FROM Jesus_2, Vatican
                   WHERE Jesus_2.ccc_number = Vatican.ccc_number
                   """)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    # Generate HTML table output
    html_table = """
    <table>
        <tr>
            {}
        </tr>
        {}
    </table>
    """.format(
        "".join(f"<th>{col}</th>" for col in columns),
        "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    )

    # Save HTML table to a file
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(html_table)

    # Close the database connection
    conn.close()

    print("HTML table generated: output.html")