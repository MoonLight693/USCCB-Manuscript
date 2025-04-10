import sqlite3
import os
import re

from dotenv import load_dotenv
load_dotenv()
DB_FILE = os.getenv("DB_NAME")

def txt_into_database(folder_path: str) -> None:
    # Connecting to sqlite 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Iterate through all .txt files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            # Sanitize table name by replacing non-alphanumeric characters with underscores
            table_name = re.sub(r'\W+', '_', os.path.splitext(file_name)[0])
            # Ensure table name matches the format used in the application
            table_name = table_name.replace('_gemini_output', '').strip('_')
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            cursor.execute(f'''
                           CREATE TABLE {table_name} (
                               reference TEXT, paragraph TEXT
                               )
                               ''')
            # Read the file and insert data into the table
            with open(file_path, "r") as f:
                for x in f:
                    y = x.split("$")
                    cursor.execute(f'''
                        INSERT INTO {table_name}(reference, paragraph) VALUES (?, ?)
                        ''', y)
            # Delete the file after processing
            os.remove(file_path)

    # Commit changes and close connection
    conn.commit()
    conn.close()

txt_into_database("State Machine Output")
