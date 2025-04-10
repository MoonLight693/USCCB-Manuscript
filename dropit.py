import sqlite3

# Connect to the SQLite database (change the database file name if necessary)
conn = sqlite3.connect('usccb_project.db')
cursor = conn.cursor()

# Drop the table
cursor.execute("DROP TABLE IF EXISTS Jesus_Christ_The_Savior_and_Redeemer_of_Humanity_V2_GPT_gemini_output")

# Commit the changes and close the connection
conn.commit()
conn.close()
