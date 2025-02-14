'''
Author: Emma Hickey
Last Date Modified: Feb 5, 2025
Description: This script is creating a SQLite database and making an SQLite table pulled from the CCC_table.txt. 
Links to additional resources:
- https://www.geeksforgeeks.org/python-sqlite-create-table/
- https://www.youtube.com/watch?v=girsuXz0yA8
'''


import sqlite3

# Connecting to sqlite 
# Create an SQLite database
conn = sqlite3.connect("usccb_project.db")
cursor = conn.cursor()

#Create the CCC table 
with open("CCC_table.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split("|")
        if len(parts) == 3:
            ccc_number, paragrapgh, txt = parts
            cursor.execute ('''
                            INSERT INTO ccc (ccc_number, paragrapgh, txt)
                            VALUES (? ? ? )
                            ''', (ccc_number, int(paragrapgh), txt ))

#Commit changes and close connection 
conn.commit()
conn.close()

print("Data inserted successfully from the file.")
            
            
            
