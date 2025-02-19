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

print("Database successfully initialized.")


'''Josh's section--------------------------------------------------------------------------------'''
def to_table(path, table_name):
    '''give the file path to the txt and the name of the table you want created in the database'''
    # Connecting to sqlite 
    # Create an SQLite database
    conn = sqlite3.connect("usccb_project.db")
    cursor = conn.cursor()
    
    #drop table if exist
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    #Create the CCC table
    cursor.execute(f'CREATE TABLE {table_name} (ccc_number txt, paragraph txt)')
    
    f = open(path, "r")
    for x in f:
        z = x.split("$")
        print(z)
        exe = f"insert into {table_name}(CCC_number, paragraph) values "
        cursor.execute(exe + '($1, $2)', z)
    
    #Commit changes and close connection 
    conn.commit()
    conn.close()