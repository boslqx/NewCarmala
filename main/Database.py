import sqlite3

# connect to database and create file Carmala
connection = sqlite3.connect('Carmala.db')

# create a cursor to execute SQL commands
cursor = connection.cursor()

# create table User_account
cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserAccount (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT NOT NULL,
        Username TEXT NOT NULL,
        Password TEXT NOT NULL
    )
''')

# commit the changes and close the connection
connection.commit()
connection.close()


