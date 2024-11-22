import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import Session
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import simpledialog

# The login function to verify user or admin credentials
def login():
    username = entry_username.get().strip()  # Trim any leading/trailing spaces
    password = entry_password.get().strip()  # Trim any leading/trailing spaces

    # Connect to the database to verify credentials
    try:
        conn = sqlite3.connect("carmala.db")
        cursor = conn.cursor()

        # First, check if the credentials match a user
        cursor.execute('''SELECT UserID FROM UserAccount WHERE Username = ? AND Password = ?''', (username, password))
        user = cursor.fetchone()

        # If no matching user is found, check if the credentials match an admin
        if not user:
            cursor.execute('''SELECT AdminID, AdminUsername, SuperAdmin FROM AdminAccount WHERE AdminUsername = ? AND AdminPassword = ?''', (username, password))
            admin = cursor.fetchone()

            if admin:
                admin_id, admin_username, is_superadmin = admin
                # Save the session data (admin_id, username, and SuperAdmin status)
                admin_data = {"admin_id": admin_id, "username": admin_username, "SuperAdmin": is_superadmin}
                Session.set_admin_session(admin_data)  # Save admin session

                messagebox.showinfo("Admin Login Success", f"Welcome {admin_username}!")

                root.destroy()  # Close the current window
                open_admin_page()  # Open home page for admin
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            user_id = user[0]
            conn.close()
            messagebox.showinfo("Login Success", "You have successfully logged in!")

            # Set session for user login
            Session.set_user_session({"user_id": user_id})

            root.destroy()  # Close the login window
            open_home(user_id)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()  # Make sure the connection is closed


# Path for the session file
ADMIN_SESSION_FILE = "AdminSession.json"

# Function to log in as admin
def admin_login():
    username = entry_username.get()
    password = entry_password.get()



# Function to generate a random 4-digit code
def generate_verification_code():
    return str(random.randint(1000, 9999))


# Send verification email function
def send_verification_email(email, code):
    try:
        # Set up the SMTP server details
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "killerpill585@gmail.com"
        sender_password = "oxey jnwo qybz etmg"

        # Compose the email
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Verification Code"
        message["From"] = sender_email
        message["To"] = email
        text = f"Your verification code is: {code}"
        part = MIMEText(text, "plain")
        message.attach(part)

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


# Function to verify the code entered by the user
def verify_code():
    global verification_code
    entered_code = entry_verification_code.get().strip()

    if entered_code == verification_code:
        messagebox.showinfo("Success", "Verification successful!")
        # After successful verification, transition to the login screen
        verification_frame.pack_forget()
        login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    else:
        messagebox.showerror("Error", "Incorrect verification code. Please try again.")

# Connect to database and create table if not exists
def create_db():
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()


# Function to log out and clear session
def sign_out():
    global logged_in_user
    logged_in_user = None  # Clear session
    open_login_window()  # Return to login window


# Function to open login window
def open_login_window():
    login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Register user and insert into database
def register_user():
    global verification_code
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
            # Connect to the database
            conn = sqlite3.connect('Carmala.db')
            cursor = conn.cursor()

            # Check if the email already exists
            cursor.execute("SELECT * FROM UserAccount WHERE Email = ?", (reg_email,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "This email is already registered. Please use a different email.")
            else:
                # Insert the new user into the database
                cursor.execute('''
                    INSERT INTO UserAccount (Email, Username, Password) 
                    VALUES (?, ?, ?)
                ''', (reg_email, reg_username, reg_password))
                conn.commit()

                # Generate verification code and send email
                verification_code = generate_verification_code()
                if send_verification_email(reg_email, verification_code):
                    messagebox.showinfo(
                        "Success",
                        "User registered successfully! Check your email for the verification code."
                    )
                    # Switch to the verification frame
                    registration_frame.pack_forget()
                    verification_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
                else:
                    messagebox.showerror("Error", "Failed to send verification email. Please try again.")
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()




# Function to open the home page (replace with actual home page code)
def open_admin_page():
    os.system('python Adminpage.py')  # This will execute the Home.py script

def open_home(user_id):
    os.system('python Home.py')


def open_registration_frame():
    # Hide the login frame
    login_frame.pack_forget()

    # Show the registration frame
    registration_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)


def forgot_password():
    global verification_code

    # Step 1: Prompt for the user's email address
    email = simpledialog.askstring("Forgot Password", "Enter your registered email:")

    if email:
        # Check if email exists in the database
        conn = sqlite3.connect('Carmala.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM UserAccount WHERE Email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Step 2: Generate and send the verification code
            verification_code = generate_verification_code()
            if send_verification_email(email, verification_code):
                # Step 3: Prompt the user to enter the verification code
                entered_code = simpledialog.askstring("Verification", "Enter the 4-digit verification code sent to your email:")

                if entered_code == verification_code:
                    # Step 4: Create a new window for password reset
                    reset_window = tk.Toplevel()
                    reset_window.title("Reset Password")

                    # Function to handle password update
                    def update_password():
                        new_password = new_password_entry.get()
                        confirm_password = confirm_password_entry.get()

                        if len(new_password) < 8 or not new_password.isalnum():
                            messagebox.showerror("Error", "Password must be at least 8 characters and contain no special characters!")
                        elif new_password != confirm_password:
                            messagebox.showerror("Error", "Passwords do not match!")
                        else:
                            # Update the password in the database
                            conn = sqlite3.connect('Carmala.db')
                            cursor = conn.cursor()
                            cursor.execute("UPDATE UserAccount SET Password = ? WHERE Email = ?", (new_password, email))
                            conn.commit()
                            conn.close()
                            messagebox.showinfo("Success", "Password updated successfully!")
                            reset_window.destroy()
                            open_login_window()  # Redirect to login window

                    # Add password entries with placeholders
                    def add_placeholder_password(entry, placeholder_text):
                        entry.insert(0, placeholder_text)
                        entry.configure(fg='grey', show='')
                        entry.bind("<FocusIn>", lambda e: clear_placeholder_password(e, placeholder_text))
                        entry.bind("<FocusOut>", lambda e: restore_placeholder_password(e, placeholder_text))

                    def clear_placeholder_password(event, placeholder_text):
                        entry = event.widget
                        if entry.get() == placeholder_text:
                            entry.delete(0, tk.END)
                            entry.configure(fg='black', show='*')

                    def restore_placeholder_password(event, placeholder_text):
                        entry = event.widget
                        if entry.get() == "":
                            entry.insert(0, placeholder_text)
                            entry.configure(fg='grey', show='')

                    # Create and pack new password entry
                    new_password_entry = tk.Entry(reset_window)
                    add_placeholder_password(new_password_entry, "Enter new password")
                    new_password_entry.pack(pady=5)

                    # Create and pack confirm password entry
                    confirm_password_entry = tk.Entry(reset_window)
                    add_placeholder_password(confirm_password_entry, "Confirm new password")
                    confirm_password_entry.pack(pady=5)

                    # Submit button
                    submit_button = tk.Button(reset_window, text="Submit", command=update_password)
                    submit_button.pack(pady=10)
                else:
                    messagebox.showerror("Error", "Incorrect verification code. Please try again.")
        else:
            # Email not registered
            messagebox.showerror("Error", "This email is not registered for the application.")


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

# Function to change button color on hover
def on_hover(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color
# Toggle password visibility
def toggle_password_visibility():
    if show_password_var.get():
        entry_password.config(show="")  # Show password
    else:
        entry_password.config(show="*")  # Hide password
# Create the main window
root = tk.Tk()
root.title("Account Login Page")
root.geometry('1000x680')
root.resizable(False, False)

# Call the function to create the database and table
create_db()

# Main Tkinter window, login and registration UI setup
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
label_title.pack(pady=100)

# Username label and entry in the login frame
label_username = tk.Label(login_frame, text="Username:", bg='#F1F1F1', font=("Poppins"))
label_username.place(x=60, y=170)

entry_username = tk.Entry(login_frame, font=("Poppins", 14), width=25)
entry_username.place(x=63, y=195)

# Add placeholder text for the username
add_placeholder(entry_username, "Enter your username")

# Password label and entry in the login frame
label_password = tk.Label(login_frame, text="Password:", bg='#F1F1F1', font=("Poppins"))
label_password.place(x=60, y=250)

entry_password = tk.Entry(login_frame, show="", font=("Poppins", 14), width=25)
entry_password.place(x=63, y=275)

# Add placeholder text for the password
add_placeholder_password(entry_password, "Enter your password")
show_password_var = tk.BooleanVar()
check_show_password = tk.Checkbutton(
    login_frame,
    text="Show Password",
    variable=show_password_var,
    command=toggle_password_visibility,
    bg="#F1F1F1",
    font=("Poppins", 10)
)
check_show_password.place(x=63, y=310)
# Login button in the login frame
button_login = tk.Button(login_frame, text="Log in",  fg="white",font=("Poppins",12,"bold"), command=login, bg="#1572D3")
button_login.bind("<Enter>", lambda event: on_hover(button_login, "#1058A7"))
button_login.bind("<Leave>", lambda event: on_leave(button_login, "#1572D3"))
button_login.place(x=180, y=340)

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
label_reg_title.pack(pady=70)

# Registration Email field
label_reg_email = tk.Label(registration_frame, text="Email:", bg='#F1F1F1', font=("Poppins"))
label_reg_email.place(x=60, y=150)
entry_reg_email = tk.Entry(registration_frame, font=("Poppins", 14), width=25)
entry_reg_email.place(x=63, y=175)

# Add placeholder text for the email
add_placeholder(entry_reg_email, "Enter your email")


# Registration Username field
label_reg_username = tk.Label(registration_frame, text="Username:", bg='#F1F1F1', font=("Poppins"))
label_reg_username.place(x=60, y=230)
entry_reg_username = tk.Entry(registration_frame, font=("Poppins", 14), width=25)
entry_reg_username.place(x=63, y=255)

# Add placeholder text for the username
add_placeholder(entry_reg_username, "Enter your username")


# Registration Password field
label_reg_password = tk.Label(registration_frame, text="Password:", bg='#F1F1F1', font=("Poppins"))
label_reg_password.place(x=60, y=310)
entry_reg_password = tk.Entry(registration_frame, show="", font=("Poppins", 14), width=25)
entry_reg_password.place(x=63, y=335)

# Add placeholder text for the password
add_placeholder_password(entry_reg_password, "Enter your password")

# Password requirements note
label_password_note = tk.Label(registration_frame, text="Minimum 8 characters, no special characters", fg="grey",
                               bg='#F1F1F1')
label_password_note.place(x=61, y=360)

# Confirm Password field
label_confirm_password = tk.Label(registration_frame, text="Confirm Password:", bg='#F1F1F1', font=("Poppins"))
label_confirm_password.place(x=60, y=410)
entry_confirm_password = tk.Entry(registration_frame, show="", font=("Poppins", 14), width=25)
entry_confirm_password.place(x=63, y=435)

# Add placeholder text for the confirm password
add_placeholder_password(entry_confirm_password, "Confirm your password")

# Confirm Password matching note
label_confirm_password_note = tk.Label(registration_frame, text="Password should be the same as above", fg="grey",
                                       bg='#F1F1F1')
label_confirm_password_note.place(x=61, y=460)

# Register button
button_register = tk.Button(registration_frame, text="Register",  fg="white",font=("Poppins",12,"bold"),command=register_user, bg="#1572D3")
button_register.bind("<Enter>", lambda event: on_hover(button_register, "#1058A7"))
button_register.bind("<Leave>", lambda event: on_leave(button_register, "#1572D3"))
button_register.place(x=170, y=500)

# Back to login button
button_back_to_login = tk.Button(registration_frame, text="Back to Login",  fg="white",font=("Poppins",12,"bold"),
                                 command=lambda: [registration_frame.pack_forget(),
                                                  login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)],
                                 bg="#1572D3")
button_back_to_login.bind("<Enter>", lambda event: on_hover(button_back_to_login, "#1058A7"))
button_back_to_login.bind("<Leave>", lambda event: on_leave(button_back_to_login, "#1572D3"))
button_back_to_login.place(x=150, y=550)


# Define the verification frame in the Tkinter UI setup
verification_frame = tk.Frame(main_frame, bg='#F1F1F1')

# Add verification code entry field
label_verification = tk.Label(verification_frame, text="Enter Verification Code:", font=("Poppins", 14), bg='#F1F1F1')
label_verification.pack(pady=20)

entry_verification_code = tk.Entry(verification_frame, font=("Poppins", 14), width=10)
entry_verification_code.pack(pady=10)

# Button to verify code
button_verify_code = tk.Button(verification_frame, text="Verify", font=("Poppins", 12, "bold"), fg="white", bg="#1572D3", command=verify_code)
button_verify_code.pack(pady=20)

# Start the main event loop
root.mainloop()