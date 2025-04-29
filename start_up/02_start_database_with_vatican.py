from Vatican.Vatican_to_SQL import *
from dotenv import load_dotenv
import os
load_dotenv()
DB_FILE = os.getenv("DB_NAME")

def start_database_with_vatican() -> None:
    # Connecting to sqlite 
    # Create an SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    #drop table if exist
    cursor.execute("DROP TABLE IF EXISTS Vatican")

    #Create the CCC table
    cursor.execute('''
                   CREATE TABLE Vatican (
                       reference txt, paragraph txt
                       )
                       ''')

    #Create the CCC table 
    f = open("start_up/Vatican/CCC_table.txt", "r", encoding="utf-8")
    for x in f:
        y = x.split("$")
        cursor.execute('''
                    insert into Vatican(reference, paragraph) values ($1, $2)
                    ''', y)

    cursor.execute(f"DROP TABLE IF EXISTS Test_text")

    #Commit changes and close connection 
    conn.commit()
    conn.close()

start_database_with_vatican()
print("Database successfully initialized.")
#to_table("/home/whitmercraft939/USCCB-Manuscript-3/State Machine Output/Test Text.txt", "Test_Text")

# Experiment