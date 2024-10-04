import sqlite3

# Create database
def connect_database():
    database = sqlite3.connect('carmala.db')
    return database


conn = connect_database()
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS User_Account (
        User_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Email TEXT,
        Username TEXT,
        Password TEXT
    )    
""")
conn.commit()

cursor.execute("INSERT INTO User_Account VALUES('1', 'boslianqx@gmail.com', 'bos', 'liangqixun')")

