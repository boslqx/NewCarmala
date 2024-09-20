import tkinter as tk
from tkinter import messagebox


def login():
    username = entry_username.get()
    password = entry_password.get()

    # Dummy check for credentials
    if username == "user" and password == "pass":
        messagebox.showinfo("Login Successful", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")


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


def clear_placeholder(event, placeholder_text):
    if event.widget.get() == placeholder_text:
        event.widget.delete(0, tk.END)
        event.widget.configure(fg='black')


def restore_placeholder(event, placeholder_text):
    if not event.widget.get():
        event.widget.insert(0, placeholder_text)
        event.widget.configure(fg='grey')

# Create the main window
root = tk.Tk()
root.title("Account Login Page")
root.state('zoomed')  # Set window to full screen

# Create a main frame for the layout
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a frame for the login page
login_frame = tk.Frame(main_frame, bg='#f8f4e3')
login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Create a frame for the green section on the right
green_frame = tk.Frame(main_frame, bg='#c6e2c6', width=400)
green_frame.pack(fill=tk.Y, side=tk.RIGHT)

# Create the title label in the login frame
label_title = tk.Label(login_frame, text="ACCOUNT LOGIN", font=("Times New Roman", 24, "bold"), bg='#f8f4e3')
label_title.pack(pady=20)

# Username label and entry in the login frame
label_username = tk.Label(login_frame, text="Username:", bg='#f8f4e3')
label_username.pack()
entry_username = tk.Entry(login_frame)
entry_username.pack(pady=5)

# Add placeholder text for the username
add_placeholder(entry_username, "Enter your username")

# Password label and entry in the login frame
label_password = tk.Label(login_frame, text="Password:", bg='#f8f4e3')
label_password.pack()
entry_password = tk.Entry(login_frame, show="")
entry_password.pack(pady=5)

# Add placeholder text for the password
add_placeholder(entry_password, "Enter your password")

# Login button in the login frame
button_login = tk.Button(login_frame, text="Log in", command=login, bg="#f5f2d0")
button_login.pack(pady=20)

# Forgot password and register labels in the login frame
label_forgot_password = tk.Label(login_frame, text="Forgot password?", fg="blue", cursor="hand2", bg='#f8f4e3')
label_forgot_password.pack(side=tk.LEFT, padx=(10, 0), anchor='s')
label_forgot_password.bind("<Button-1>", lambda e: forgot_password())

label_register = tk.Label(login_frame, text="Don’t have an account? Register now", fg="blue", cursor="hand2",bg='#f8f4e3')
label_register.pack(side=tk.RIGHT, padx=(0, 10), anchor='s')
label_register.bind("<Button-1>", lambda e: open_registration_frame())

# Create a frame for the registration page
registration_frame = tk.Frame(main_frame, bg='#f8f4e3')

# Registration form title
label_reg_title = tk.Label(registration_frame, text="REGISTER", font=("Times New Roman", 24, "bold"), bg='#f8f4e3')
label_reg_title.pack(pady=20)

# Registration Email field
label_reg_email = tk.Label(registration_frame, text="Email:", bg='#f8f4e3')
label_reg_email.pack()
entry_reg_email = tk.Entry(registration_frame)
entry_reg_email.pack(pady=5)

# Registration Username field
label_reg_username = tk.Label(registration_frame, text="Username:", bg='#f8f4e3')
label_reg_username.pack()
entry_reg_username = tk.Entry(registration_frame)
entry_reg_username.pack(pady=5)

# Registration Password field
label_reg_password = tk.Label(registration_frame, text="Password:", bg='#f8f4e3')
label_reg_password.pack()
entry_reg_password = tk.Entry(registration_frame, show="")
entry_reg_password.pack(pady=5)

# Password requirements note
label_password_note = tk.Label(registration_frame, text="Minimum 8 characters, no special characters", fg="grey", bg='#f8f4e3')
label_password_note.pack()

# Confirm Password field
label_confirm_password = tk.Label(registration_frame, text="Confirm Password:", bg='#f8f4e3')
label_confirm_password.pack()
entry_confirm_password = tk.Entry(registration_frame, show="")
entry_confirm_password.pack(pady=5)

# Confirm Password matching note
label_confirm_password_note = tk.Label(registration_frame, text="Password should be the same as above", fg="grey", bg='#f8f4e3')
label_confirm_password_note.pack()

# Register button
button_register = tk.Button(registration_frame, text="Register", command=register_user, bg="#f5f2d0")
button_register.pack(pady=20)

# Back to login button
button_back_to_login = tk.Button(registration_frame, text="Back to Login",
command=lambda: [registration_frame.pack_forget(), login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)], bg="#f5f2d0")
button_back_to_login.pack(pady=10)

# Start the main event loop
root.mainloop()

