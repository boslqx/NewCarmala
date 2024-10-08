import sqlite3

# Connect to the Carmala database
connection = sqlite3.connect('Carmala.db')
cursor = connection.cursor()

# Insert some user account data
user_data = [
    ("admin_avis", "bffuJkfs34", "avis@gmail.com"),
    ("admin_klook", "ljoNjN3k5b", "klook@gmail.com"),
    ("admin_kayak", "MausoH1i3h", "kayak@gmailx.com")
]

# Insert data into UserAccount table
cursor.executemany('''
    INSERT INTO AdminAccount (Admin_username, Admin_password, Admin_email)
    VALUES (?, ?, ?)
''', user_data)

connection.commit()
connection.close()

print("User accounts inserted successfully.")

