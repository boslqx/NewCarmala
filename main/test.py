import os
import sqlite3
from tkinter import messagebox

def login():
    username = entry_username.get().strip()  # Trim any leading/trailing spaces
    password = entry_password.get().strip()  # Trim any leading/trailing spaces

    # Connect to the database to verify credentials
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    # First, check if the credentials match a user
    cursor.execute('''
        SELECT UserID FROM UserAccount WHERE Username = ? AND Password = ?
    ''', (username, password))
    user = cursor.fetchone()

    # If no matching user is found, check if the credentials match an admin
    if not user:
        cursor.execute('''
            SELECT * FROM AdminAccount WHERE AdminUsername = ? AND AdminPassword = ?
        ''', (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            messagebox.showinfo("Admin Login Success", "Welcome Admin!")
            root.destroy()  # Close the current window
            open_admin_page()  # Open home page for admin
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")  # Neither user nor admin credentials matched
            return None
    else:
        user_id = user[0]  # Get the UserID from the result
        conn.close()
        messagebox.showinfo("Login Success", "You have successfully logged in!")

        root.destroy()  # Close the current window

        # Open the home page for the user and pass the UserID as a command-line argument
        os.system(f'python Home.py {user_id}')  # Pass UserID to Home.py

        return user_id  # Return UserID to use later, if necessary
