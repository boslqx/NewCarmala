import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from main.Database import connect_database


def save_useraccount_data(email, username, password):
    try:
        # Connect to the database
        conn = connect_database()
        cursor = conn.cursor()

        # Ensure the User_Account table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS User_Account (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Email TEXT NOT NULL,
                Username TEXT NOT NULL UNIQUE,  -- Ensures unique usernames
                Password TEXT NOT NULL
            )
        """)
        print("Table check/creation succeeded.")  # Debugging message

        # Insert user data into the User_Account table
        cursor.execute("""
            INSERT INTO User_Account (Email, Username, Password)
            VALUES (?, ?, ?)
        """, (email, username, password))

        conn.commit()  # Ensure the transaction is saved to the database
        conn.close()

        # Inform the user of success
        messagebox.showinfo("Success", "Account registered successfully!")
    except Exception as e:
        print(f"Error saving user account: {e}")  # Debugging output
        messagebox.showerror("Database Error", f"An error occurred: {e}")



def register_user():
    # Fetch user inputs
    reg_email = entry_reg_email.get().strip()  # Remove spaces
    reg_username = entry_reg_username.get().strip()  # Remove spaces
    reg_password = entry_reg_password.get().strip()  # Remove spaces
    confirm_password = entry_confirm_password.get().strip()  # Remove spaces

    # Validation for password
    if reg_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
    elif len(reg_password) < 8 or not reg_password.isalnum():
        messagebox.showerror("Error", "Password must be at least 8 characters and contain no special characters!")
    else:
        try:
            # Save the account to the database
            save_useraccount_data(reg_email, reg_username, reg_password)
            # After registering, return to the login frame
            registration_frame.pack_forget()
            login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        except Exception as e:
            messagebox.showerror("Registration Failed", f"Error during registration: {e}")



def login():
    username = entry_username.get().strip()  # Trim any leading/trailing spaces
    password = entry_password.get().strip()  # Trim any leading/trailing spaces

    try:
        conn = connect_database()
        cursor = conn.cursor()

        # Retrieve user data from the database
        cursor.execute("""
            SELECT * FROM User_Account WHERE Username = ? AND Password = ?
        """, (username, password))

        user = cursor.fetchone()  # Fetch a single matching row
        conn.close()

        # Debugging output to check what was retrieved
        if user:
            print(f"User found: {user}")
            messagebox.showinfo("Login Successful", "Welcome!")
        else:
            print(f"Login failed for Username: {username}, Password: {password}")
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


def open_registration_frame():
    # Hide the login frame
    login_frame.pack_forget()

    # Show the registration frame
    registration_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)


def register_user():
    # Dummy function for registration
    reg_email = entry_reg_email.get()
    reg_username = entry_reg_username.get()
    reg_password = entry_reg_password.get()
    confirm_password = entry_confirm_password.get()

    # Simple check for matching passwords
    if reg_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
    elif len(reg_password) < 8 or not reg_password.isalnum():
        messagebox.showerror("Error", "Password must be at least 8 characters and contain no special characters!")
    else:
        messagebox.showinfo("Register", f"User {reg_username} registered successfully!")
        # After registering, return to the login frame
        registration_frame.pack_forget()
        login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)


def forgot_password():
    messagebox.showinfo("Forgot Password", "Redirecting to password recovery...")


def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.configure(fg='grey')
    entry.bind("<FocusIn>", lambda event: clear_placeholder(event, placeholder_text))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(event, placeholder_text))

def add_placeholder_password(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.configure(fg='grey')
    entry.bind("<FocusIn>", lambda event: clear_placeholder_password(event, placeholder_text))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(event, placeholder_text))


def clear_placeholder(event, placeholder_text):
    if event.widget.get() == placeholder_text:
        event.widget.delete(0, tk.END)
        event.widget.configure(fg='black')

def clear_placeholder_password(event, placeholder_text):
    if event.widget.get() == placeholder_text:
        event.widget.delete(0, tk.END)
        event.widget.configure(fg="black", show="*")


def restore_placeholder(event, placeholder_text):
    if not event.widget.get():
        event.widget.insert(0, placeholder_text)
        event.widget.configure(fg='grey')


# Create the main window
root = tk.Tk()
root.title("Account Login Page")
root.geometry('1280x700')

# Create a main frame for the layout
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a frame for the login page
login_frame = tk.Frame(main_frame, bg='#F1F1F1')
login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Create a frame for image on the right
right_frame = tk.Frame(main_frame, bg='#F1F1F1', width=400)
image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-24 200101.png"
image = Image.open(image_path)
image = ImageTk.PhotoImage(image)

image_label = tk.Label(right_frame, image=image)
image_label.pack(fill=tk.BOTH, expand=True)
right_frame.pack(fill=tk.Y, side=tk.RIGHT)

# Create the title label in the login frame
label_title = tk.Label(login_frame, text="Login", font=("Poppins", 24, "bold"), bg='#F1F1F1')
label_title.pack(pady=20)

# Username label and entry in the login frame
label_username = tk.Label(login_frame, text="Username:", bg='#F1F1F1')
label_username.pack()
entry_username = tk.Entry(login_frame)
entry_username.pack(pady=5)

# Add placeholder text for the username
add_placeholder(entry_username, "Enter your username")

# Password label and entry in the login frame
label_password = tk.Label(login_frame, text="Password:", bg='#F1F1F1')
label_password.pack()
entry_password = tk.Entry(login_frame, show="")
entry_password.pack(pady=5)

# Add placeholder text for the password
add_placeholder_password(entry_password, "Enter your password")

# Login button in the login frame
button_login = tk.Button(login_frame, text="Log in", font="Poppins", command=login, bg="#1572D3")
button_login.pack(pady=20)

# Forgot password and register labels in the login frame
label_forgot_password = tk.Label(login_frame, text="Forgot password?", fg="black", cursor="hand2", bg='#F1F1F1')
label_forgot_password.pack(side=tk.LEFT, padx=(10, 0), anchor='s')
label_forgot_password.bind("<Button-1>", lambda e: forgot_password())

label_register = tk.Label(login_frame, text="Don’t have an account? Register now", fg="black", cursor="hand2",
                          bg='#F1F1F1')
label_register.pack(side=tk.RIGHT, padx=(0, 10), anchor='s')
label_register.bind("<Button-1>", lambda e: open_registration_frame())

# Create a frame for the registration page
registration_frame = tk.Frame(main_frame, bg='#F1F1F1')

# Registration form title
label_reg_title = tk.Label(registration_frame, text="Register", font=("Poppins", 24, "bold"), bg='#F1F1F1')
label_reg_title.pack(pady=20)

# Registration Email field
label_reg_email = tk.Label(registration_frame, text="Email:", bg='#F1F1F1')
label_reg_email.pack()
entry_reg_email = tk.Entry(registration_frame)
entry_reg_email.pack(pady=5)

# Add placeholder text for the email
add_placeholder(entry_reg_email, "Enter your username")


# Registration Username field
label_reg_username = tk.Label(registration_frame, text="Username:", bg='#F1F1F1')
label_reg_username.pack()
entry_reg_username = tk.Entry(registration_frame)
entry_reg_username.pack(pady=5)

# Add placeholder text for the username
add_placeholder(entry_reg_username, "Enter your username")


# Registration Password field
label_reg_password = tk.Label(registration_frame, text="Password:", bg='#F1F1F1')
label_reg_password.pack()
entry_reg_password = tk.Entry(registration_frame, show="")
entry_reg_password.pack(pady=5)

# Add placeholder text for the password
add_placeholder_password(entry_reg_password, "Enter your password")

# Password requirements note
label_password_note = tk.Label(registration_frame, text="Minimum 8 characters, no special characters", fg="grey",
                               bg='#F1F1F1')
label_password_note.pack()

# Confirm Password field
label_confirm_password = tk.Label(registration_frame, text="Confirm Password:", bg='#F1F1F1')
label_confirm_password.pack()
entry_confirm_password = tk.Entry(registration_frame, show="")
entry_confirm_password.pack(pady=5)

# Add placeholder text for the confirm password
add_placeholder_password(entry_confirm_password, "Enter your username")

# Confirm Password matching note
label_confirm_password_note = tk.Label(registration_frame, text="Password should be the same as above", fg="grey",
                                       bg='#F1F1F1')
label_confirm_password_note.pack()

# Register button
button_register = tk.Button(registration_frame, text="Register", font="Poppins",command=register_user, bg="#1572D3")
button_register.pack(pady=20)

# Back to login button
button_back_to_login = tk.Button(registration_frame, text="Back to Login",  font="Poppins",
                                 command=lambda: [registration_frame.pack_forget(),
                                                  login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)],
                                 bg="#1572D3")
button_back_to_login.pack(pady=10)

# Start the main event loop
root.mainloop()
