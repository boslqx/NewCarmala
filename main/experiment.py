import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import sqlite3
import subprocess
import Session
import os
import io

# Retrieve the logged-in user
user_data = Session.get_user_session()
if user_data:
    user_id = user_data["user_id"]
    print(f"Logged in as User ID: {user_id}")
else:
    print("No user is logged in.")

# Global variables for file paths
profile_picture_path = None
driving_license_path = None

# Function to convert image file to BLOB (binary data)
def convert_image_to_blob(file_path):
    with open(file_path, 'rb') as file:
        blob_data = file.read()
    return blob_data

# Function to save user data to the database
def save_to_database():
    user_id = user_data["user_id"]
    username = username_entry.get().strip()
    email = email_entry.get().strip()
    gender = gender_combobox.get()
    country = country_entry.get().strip()
    identification_number = id_entry.get().strip()

    profile_picture = convert_image_to_blob(profile_picture_path) if profile_picture_path else None
    driving_license = convert_image_to_blob(driving_license_path) if driving_license_path else None

    # Open the connection to the database
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    # Update the user's data, including profile picture and driving license
    cursor.execute('''
        UPDATE UserAccount
        SET Username = ?, Email = ?, Gender = ?, Country = ?, IdentificationNumber = ?, ProfilePicture = ?, DrivingLicense = ?
        WHERE UserID = ?
    ''', (username, email, gender, country, identification_number, profile_picture, driving_license, user_id))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "User profile updated successfully!")
    toggle_edit(False)  # Disable editing after saving

# Function to load user data into fields
def load_user_data():
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Username, Email, Gender, Country, IdentificationNumber, ProfilePicture, DrivingLicense FROM UserAccount WHERE UserID = ?",
        (user_id,))
    user_info = cursor.fetchone()
    conn.close()

    print("Fetched user data:", user_info)  # Debugging output

    if user_info:
        # Temporarily enable editing to populate the fields, then disable again if needed
        username_entry.config(state='normal')
        email_entry.config(state='normal')
        country_entry.config(state='normal')
        id_entry.config(state='normal')

        # Clear existing values and insert fetched data
        username_entry.delete(0, tk.END)
        username_entry.insert(0, user_info[0] or "")

        email_entry.delete(0, tk.END)
        email_entry.insert(0, user_info[1] or "")

        gender_combobox.set(user_info[2] or "")

        country_entry.delete(0, tk.END)
        country_entry.insert(0, user_info[3] or "")

        id_entry.delete(0, tk.END)
        id_entry.insert(0, user_info[4] or "")

        # Disable editing if not in edit mode
        username_entry.config(state='readonly')
        email_entry.config(state='readonly')
        country_entry.config(state='readonly')
        id_entry.config(state='readonly')

        # Display profile picture if available
        if user_info[5]:
            profile_img_data = io.BytesIO(user_info[5])
            profile_img = Image.open(profile_img_data)
            profile_img = profile_img.resize((100, 100), Image.LANCZOS)
            profile_img_display = ImageTk.PhotoImage(profile_img)
            profile_picture_label.config(image=profile_img_display)
            profile_picture_label.image = profile_img_display

        # Display driving license image if available
        if user_info[6]:
            license_img_data = io.BytesIO(user_info[6])
            license_img = Image.open(license_img_data)
            license_img = license_img.resize((100, 100), Image.LANCZOS)
            license_img_display = ImageTk.PhotoImage(license_img)
            driving_license_label.config(image=license_img_display)
            driving_license_label.image = license_img_display
    else:
        messagebox.showwarning("Warning", "User information could not be retrieved.")


# Function to toggle editing
def toggle_edit(state):
    username_entry.config(state='normal' if state else 'readonly')
    email_entry.config(state='normal' if state else 'readonly')
    gender_combobox.config(state='normal' if state else 'readonly')
    country_entry.config(state='normal' if state else 'readonly')
    id_entry.config(state='normal' if state else 'readonly')
    upload_profile_btn.config(state='normal' if state else 'disabled')
    upload_license_btn.config(state='normal' if state else 'disabled')
    save_btn.config(state='normal' if state else 'disabled')
    edit_btn.config(state='disabled' if state else 'normal')

# Functions to upload files
def upload_profile_picture():
    global profile_picture_path
    file_path = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        profile_picture_path = file_path

def upload_driving_license():
    global driving_license_path
    file_path = filedialog.askopenfilename(title="Select Driving License", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        driving_license_path = file_path

# Function to log out and return to login window
def log_out():
    Session.clear_user_session()
    root.destroy()
    subprocess.Popen(["python", "Login.py"])

# Function to open the selected button
def open_home():
    root.destroy()
    os.system('python Home.py')

# Function to open the script when the "How it Works" button is clicked
def open_howitworks():
    process = subprocess.Popen(["python", "How it Works.py"])
    print("How it Works opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(300, root.destroy)  # Waits 300 milliseconds (1 second) before destroying

# Function to open the script when the "Become a Renter" button is clicked
def open_becomearenter():
    process = subprocess.Popen(["python", "Become a renter.py"])
    print("Become a renter opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(300, root.destroy)  # Waits 300 milliseconds (1 second) before destroying
# Function to open the selected button
def open_bookingdetails():
    process = subprocess.Popen(["python", "Booking details.py"])
    print("Booking details opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(300, root.destroy)  # Waits 300 milliseconds (1 second) before destroying


# GUI setup
root = tk.Tk()
root.title("User Profile")
root.geometry("1100x700")

# Create main canvas
canvas = tk.Canvas(root, width=1000, height=700)
canvas.pack(fill='both', expand=True)

# Load logo and add it to the canvas
logo_path = r"C:\Users\User\OneDrive\Pictures\Saved Pictures\cleaned_image.png"
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((150, 100), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)
logo_button = tk.Label(root, image=logo_photo, cursor="hand2", bg="#F1F1F1")
canvas.create_window(10, 2, anchor="nw", window=logo_button)
logo_button.bind("<Button-1>", lambda e: open_home())

# Header buttons
become_renter_button = tk.Button(root, bg="#1572D3", text="Become a Renter", fg="white", font=("Poppins", 12, "bold"), command=open_becomearenter)
canvas.create_window(200, 40, anchor="nw", window=become_renter_button)

how_it_works_button = tk.Button(root, bg="#1572D3", text="How It Works", fg="white", font=("Poppins", 12, "bold"), command=open_howitworks)
canvas.create_window(370, 40, anchor="nw", window=how_it_works_button)

bookingdetails_button = tk.Button(root, bg="#1572D3", text="Booking Details", fg="white", font=("Poppins", 12, "bold"), command=open_bookingdetails)
canvas.create_window(510, 40, anchor="nw", window=bookingdetails_button)

log_out_button = tk.Button(root, bg="#1572D3", text="Log Out", fg="white", font=("Poppins", 12, "bold"), command=log_out)
canvas.create_window(960, 40, anchor="nw", window=log_out_button)

# User information fields
username_entry = ttk.Entry(root, width=40)
email_entry = ttk.Entry(root, width=40)
gender_combobox = ttk.Combobox(root, values=["Male", "Female", "Other"], width=40, state='readonly')
country_entry = ttk.Entry(root, width=40)
id_entry = ttk.Entry(root, width=40)

# Profile picture and driving license image labels
profile_picture_label = tk.Label(root, bg="white", width=100, height=100)
driving_license_label = tk.Label(root, bg="white", width=150, height=100)

# Add blue rectangle (header) decoration
canvas.create_rectangle(0, 120, 1500, 200, fill="#1572D3", outline="")

# Layout
canvas.create_window(200, 350, window=ttk.Label(root, text="Username", font=("Poppins", 12)))
canvas.create_window(400, 350, window=username_entry)
canvas.create_window(700, 350, window=ttk.Label(root, text="Email", font=("Poppins", 12)))
canvas.create_window(900, 350, window=email_entry)
canvas.create_window(200, 420, window=ttk.Label(root, text="Gender", font=("Poppins", 12)))
canvas.create_window(400, 420, window=gender_combobox)
canvas.create_window(700, 420, window=ttk.Label(root, text="Country", font=("Poppins", 12)))
canvas.create_window(900, 420, window=country_entry)
canvas.create_window(700, 500, window=ttk.Label(root, text="ID Number", font=("Poppins", 12)))
canvas.create_window(900, 500, window=id_entry)

# Display profile picture and driving license images
canvas.create_window(380, 260, window=profile_picture_label)
canvas.create_window(400, 500, window=driving_license_label)

# Buttons for uploading files
upload_profile_btn = ttk.Button(root, text="Upload Profile Picture", command=upload_profile_picture)
canvas.create_window(200, 260, window=upload_profile_btn)
upload_license_btn = ttk.Button(root, text="Upload Driving License", command=upload_driving_license)
canvas.create_window(180, 500, window=upload_license_btn)




# Edit and Save buttons
edit_btn = tk.Button(root, width=10, height=2,text="Edit", bg="#1572D3", fg="white", font=("Arial", 12, "bold"),command=lambda: toggle_edit(True))
save_btn = tk.Button(root, width=10, height=2,text="Save", bg="#1572D3", fg="white", font=("Arial", 12, "bold"), command=save_to_database)
canvas.create_window(980, 200, window=edit_btn)
canvas.create_window(550, 600, window=save_btn)

# Initialize UI
toggle_edit(False)  # Disable editing by default
load_user_data()  # Load the user's data into the fields

root.mainloop()
