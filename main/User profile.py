import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import sqlite3
import subprocess
import Session
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

    # Debugging: Print the values being retrieved from entry widgets
    print(f"Saving data for User ID {user_id}:")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Gender: {gender}")
    print(f"Country: {country}")
    print(f"ID Number: {identification_number}")

    # Only convert image to BLOB if a new file was uploaded
    profile_picture = convert_image_to_blob(profile_picture_path) if profile_picture_path else None
    driving_license = convert_image_to_blob(driving_license_path) if driving_license_path else None

    try:
        with sqlite3.connect('Carmala.db') as conn:
            cursor = conn.cursor()

            # Get the current images in the database to avoid overwriting if no new image is uploaded
            cursor.execute("SELECT ProfilePicture, DrivingLicense FROM UserAccount WHERE UserID = ?", (user_id,))
            current_images = cursor.fetchone()
            current_profile_picture = current_images[0] if current_images[0] else None
            current_driving_license = current_images[1] if current_images[1] else None

            # If no new image is uploaded, keep the old images in the database
            profile_picture = profile_picture if profile_picture else current_profile_picture
            driving_license = driving_license if driving_license else current_driving_license

            # Update user's data
            cursor.execute('''UPDATE UserAccount
                              SET Username = ?, Email = ?, Gender = ?, Country = ?, IdentificationNumber = ?, ProfilePicture = ?, DrivingLicense = ?
                              WHERE UserID = ?''',
                           (username, email, gender, country, identification_number, profile_picture, driving_license, user_id))

            conn.commit()  # Commit the transaction after both updates
            messagebox.showinfo("Success", "User profile updated successfully!")
            toggle_edit(False)  # Disable editing after saving
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        messagebox.showerror("Error", f"Error saving data: {e}")



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

        # Set placeholders if profile picture or driving license is missing
        placeholder_img = Image.new('RGB', (100, 100), color='gray')  # Creates a gray square placeholder image
        placeholder_img_display = ImageTk.PhotoImage(placeholder_img)

        # Display profile picture
        if user_info[5]:  # If profile picture exists
            profile_img_data = io.BytesIO(user_info[5])
            profile_img = Image.open(profile_img_data)
            profile_img = profile_img.resize((100, 100), Image.LANCZOS)
            profile_img_display = ImageTk.PhotoImage(profile_img)
        else:  # If no profile picture, use placeholder
            profile_img_display = placeholder_img_display

        # Update the profile picture label with the actual image or placeholder
        profile_picture_label.config(image=profile_img_display)
        profile_picture_label.image = profile_img_display  # Keep a reference to prevent garbage collection

        # Display driving license
        if user_info[6]:  # If driving license image exists
            license_img_data = io.BytesIO(user_info[6])
            license_img = Image.open(license_img_data)
            license_img = license_img.resize((100, 100), Image.LANCZOS)
            license_img_display = ImageTk.PhotoImage(license_img)
        else:  # If no driving license, use placeholder
            license_img_display = placeholder_img_display

        # Update the driving license label with the actual image or placeholder
        driving_license_label.config(image=license_img_display)
        driving_license_label.image = license_img_display  # Keep a reference to prevent garbage collection
    else:
        messagebox.showwarning("Warning", "User information could not be retrieved.")


# Function to toggle editing
def toggle_edit(state):
    username_entry.config(state='normal' if state else 'readonly')
    gender_combobox.config(state='normal' if state else 'readonly')
    country_entry.config(state='normal' if state else 'readonly')
    id_entry.config(state='normal' if state else 'readonly')
    upload_profile_btn.config(state='normal' if state else 'disabled')
    upload_license_btn.config(state='normal' if state else 'disabled')
    save_btn.config(state='normal' if state else 'disabled')
    edit_btn.config(state='disabled' if state else 'normal')

    # Ensure email_entry remains readonly regardless of the state
    email_entry.config(state='readonly')

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


# Function to change button color on hover
def on_hover(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color

# Window setup
root = tk.Tk()
root.title("User Profile")
root.geometry("1100x700")
root.resizable(False, False)

# Create main canvas
canvas = tk.Canvas(root, width=1000, height=700)
canvas.pack(fill='both', expand=True)

# Header buttons
home_button = tk.Button(root, bg="#1572D3",width=15, text="Back to Home", fg="white", font=("Poppins", 12, "bold"), command=open_home)
home_button.bind("<Enter>", lambda event: on_hover(home_button, "#1058A7"))
home_button.bind("<Leave>", lambda event: on_leave(home_button, "#1572D3"))
canvas.create_window(50, 40, anchor="nw", window=home_button)

log_out_button = tk.Button(root, bg="#1572D3",width=12, text="Log Out", fg="white", font=("Poppins", 12, "bold"), command=log_out)
log_out_button.bind("<Enter>", lambda event: on_hover(log_out_button, "#1058A7"))
log_out_button.bind("<Leave>", lambda event: on_leave(log_out_button, "#1572D3"))
canvas.create_window(940, 40, anchor="nw", window=log_out_button)

# User information fields
username_entry = ttk.Entry(root, width=40)
email_entry = ttk.Entry(root, width=40)
gender_combobox = ttk.Combobox(root, values=["Male", "Female", "Other"], width=40, state='readonly')
country_entry = ttk.Entry(root, width=40)
id_entry = ttk.Entry(root, width=40)

# Profile picture and driving license image labels
profile_picture_label = tk.Label(root, bg="white", width=130, height=130)
driving_license_label = tk.Label(root, bg="white", width=150, height=100)

# Add blue rectangle (header) decoration
canvas.create_rectangle(0, 0, 1500, 260, fill="#1572D3", outline="")

# Layout
canvas.create_window(200, 300, window=ttk.Label(root, text="Username", font=("Poppins", 10)))
canvas.create_window(315, 330, window=username_entry,width=300, height=40)
canvas.create_window(700, 300, window=ttk.Label(root, text="Email", font=("Poppins", 10)))
canvas.create_window(830, 330, window=email_entry,width=300, height=40)
canvas.create_window(190, 400, window=ttk.Label(root, text="Gender", font=("Poppins", 10)))
canvas.create_window(317, 430, window=gender_combobox,width=300, height=40)
canvas.create_window(700, 400, window=ttk.Label(root, text="Country", font=("Poppins", 10)))
canvas.create_window(825, 430, window=country_entry,width=300, height=40)
canvas.create_window(710, 500, window=ttk.Label(root, text="ID Number", font=("Poppins", 10)))
canvas.create_window(830, 530, window=id_entry,width=300, height=40)

# Display profile picture and driving license images
canvas.create_window(220, 180, window=profile_picture_label)
canvas.create_window(240, 550, window=driving_license_label)

# Buttons for uploading files
upload_profile_btn = ttk.Button(root, text="Upload Profile Picture", command=upload_profile_picture)
canvas.create_window(360, 195, window=upload_profile_btn)
upload_license_btn = ttk.Button(root, text="Upload Driving License", command=upload_driving_license)
canvas.create_window(390, 550, window=upload_license_btn)

# Edit and Save buttons
edit_btn = tk.Button(root, width=10, height=2,text="Edit", bg="#1572D3", fg="white", font=("Arial", 12, "bold"),command=lambda: toggle_edit(True))
save_btn = tk.Button(root, width=10, height=2,text="Save", bg="#1572D3", fg="white", font=("Arial", 12, "bold"), command=save_to_database)
canvas.create_window(850, 200, window=edit_btn)
canvas.create_window(980, 200, window=save_btn)

# Initialize UI
toggle_edit(False)  # Disable editing by default
load_user_data()  # Load the user's data into the fields

root.mainloop()
