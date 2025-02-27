from Vatican.Vatican_to_SQL import *

def start_database_with_vatican() -> None:
    # Connecting to sqlite 
    # Create an SQLite database
    conn = sqlite3.connect("usccb_project.db")
    cursor = conn.cursor()

    #drop table if exist
    cursor.execute("DROP TABLE IF EXISTS Vatican")

    #Create the CCC table
    cursor.execute('''
                   CREATE TABLE Vatican (
                       ccc_number txt, paragraph txt
                       )
                       ''')

    #Create the CCC table 
    f = open("/home/whitmercraft939/USCCB-Manuscript-3/Vatican/CCC_table.txt", "r")
    for x in f:
        y = x.split("$")
        cursor.execute('''
                    insert into Vatican(CCC_number, paragraph) values ($1, $2)
                    ''', y)

    cursor.execute(f"DROP TABLE IF EXISTS Test_text")

    #Commit changes and close connection 
    conn.commit()
    conn.close()

start_database_with_vatican()
print("Database successfully initialized.")
#to_table("/home/whitmercraft939/USCCB-Manuscript-3/State Machine Output/Test Text.txt", "Test_Text")

# Experiment