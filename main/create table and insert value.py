import sqlite3

# Connect to the database
connection = sqlite3.connect('Database.db')
cursor = connection.cursor()

# Check if the table exists or create it
cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserAccount (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT NOT NULL,
        Username TEXT NOT NULL,
        Password TEXT NOT NULL,
        ProfilePicture BLOB,
        Gender TEXT,
        Country TEXT,
        DrivingLicense BLOB,
        IdentificationNumber TEXT    
    )
''')

# Insert test data (optional)
cursor.execute('''
    INSERT INTO UserAccount (Email, Username, Password)
    VALUES (?, ?, ?)
''', ('test@example.com', 'testuser', 'password123'))

# Query the data to check if the table is working
cursor.execute("SELECT * FROM UserAccount")
rows = cursor.fetchall()

print(rows)  # This will print the contents of the UserAccount table

# Commit the changes and close the connection
connection.commit()
connection.close()
