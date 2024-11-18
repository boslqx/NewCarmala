import customtkinter as ctk
from tkinter import filedialog, messagebox
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

    profile_picture = convert_image_to_blob(profile_picture_path) if profile_picture_path else None
    driving_license = convert_image_to_blob(driving_license_path) if driving_license_path else None

    try:
        with sqlite3.connect('Carmala.db') as conn:
            cursor = conn.cursor()

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
# Function to load user data into fields
def load_user_data():
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Username, Email, Gender, Country, IdentificationNumber, ProfilePicture, DrivingLicense FROM UserAccount WHERE UserID = ?",
                   (user_id,))
    user_info = cursor.fetchone()
    conn.close()

    print("Fetched user data:", user_info)  # Debugging output

    if user_info:
        # Temporarily enable editing to populate the fields, then disable again if needed
        username_entry.configure(state='normal')
        email_entry.configure(state='normal')
        country_entry.configure(state='normal')
        id_entry.configure(state='normal')

        # Clear existing values and insert fetched data
        username_entry.delete(0, ctk.END)
        username_entry.insert(0, user_info[0] or "")

        email_entry.delete(0, ctk.END)
        email_entry.insert(0, user_info[1] or "")

        gender_combobox.set(user_info[2] or "")

        country_entry.delete(0, ctk.END)
        country_entry.insert(0, user_info[3] or "")

        id_entry.delete(0, ctk.END)
        id_entry.insert(0, user_info[4] or "")

        # Disable editing if not in edit mode
        username_entry.configure(state='readonly')
        email_entry.configure(state='readonly')
        country_entry.configure(state='readonly')
        id_entry.configure(state='readonly')

        # Set placeholders if profile picture or driving license is missing
        placeholder_img = Image.new('RGB', (100, 100), color='gray')  # Creates a gray square placeholder image
        placeholder_img_display = ImageTk.PhotoImage(placeholder_img)

        # Remove any previously added images (if necessary)
        canvas.delete("profile_picture")  # Delete any previous profile picture from the canvas
        canvas.delete("driving_license")  # Delete any previous driving license from the canvas

        # Display profile picture
        if user_info[5] and len(user_info[5]) > 0:  # Check if ProfilePicture is not None or empty
            profile_img_data = io.BytesIO(user_info[5])
            profile_img = Image.open(profile_img_data)
            profile_img = profile_img.resize((100, 100), Image.LANCZOS)
            profile_img_display = ImageTk.PhotoImage(profile_img)
            # Display the image directly on the canvas without a label
            canvas.create_image(300, 220, image=profile_img_display, tags="profile_picture")
            canvas.image = profile_img_display  # Keep reference to avoid garbage collection
        else:
            # Handle case where ProfilePicture is missing
            placeholder_img = Image.new('RGB', (100, 100), color='gray')  # Creates a gray square placeholder image
            placeholder_img_display = ImageTk.PhotoImage(placeholder_img)
            canvas.create_image(300, 220, image=placeholder_img_display, tags="profile_picture")
            canvas.image = placeholder_img_display  # Keep reference to avoid garbage collection

        # Display driving license
        if user_info[6]:  # If driving license image exists
            license_img_data = io.BytesIO(user_info[6])
            license_img = Image.open(license_img_data)
            license_img = license_img.resize((100, 100), Image.LANCZOS)
            license_img_display = ImageTk.PhotoImage(license_img)
            # Display the image directly on the canvas without a label
            canvas.create_image(300, 690, image=license_img_display, tags="driving_license")
            canvas.image = license_img_display  # Keep reference to avoid garbage collection
        else:  # If no driving license, use placeholder
            canvas.create_image(300, 690, image=placeholder_img_display, tags="driving_license")
            canvas.image = placeholder_img_display  # Keep reference to avoid garbage collection
    else:
        messagebox.showwarning("Warning", "User information could not be retrieved.")





# Function to toggle editing
def toggle_edit(state):
    username_entry.configure(state='normal' if state else 'readonly')
    email_entry.configure(state='normal' if state else 'readonly')
    gender_combobox.configure(state='normal' if state else 'readonly')
    country_entry.configure(state='normal' if state else 'readonly')
    id_entry.configure(state='normal' if state else 'readonly')
    upload_profile_btn.configure(state='normal' if state else 'disabled')
    upload_license_btn.configure(state='normal' if state else 'disabled')
    save_btn.configure(state='normal' if state else 'disabled')
    edit_btn.configure(state='disabled' if state else 'normal')

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
    button.configure(bg_color=color)

def on_leave(button, color):
    button.configure(bg_color=color)

# GUI setup
root = ctk.CTk()
root.title("User Profile")
root.geometry("1100x700")

# Create main canvas
canvas = ctk.CTkCanvas(root, width=1000, height=700)
canvas.pack(fill='both', expand=True)

# Header buttons
home_button = ctk.CTkButton(root, text="Back to Home", text_color="white", font=("Poppins", 12, "bold"), command=open_home)
home_button.bind("<Enter>", lambda event: on_hover(home_button, "#1058A7"))
home_button.bind("<Leave>", lambda event: on_leave(home_button, "#1572D3"))
canvas.create_window(50, 40, anchor="nw", window=home_button)

log_out_button = ctk.CTkButton(root, text="Log Out", text_color="white", font=("Poppins", 12, "bold"), command=log_out)
log_out_button.bind("<Enter>", lambda event: on_hover(log_out_button, "#1058A7"))
log_out_button.bind("<Leave>", lambda event: on_leave(log_out_button, "#1572D3"))
canvas.create_window(1160, 40, anchor="nw", window=log_out_button)

# User information fields
username_entry = ctk.CTkEntry(root, width=300, height=40)
email_entry = ctk.CTkEntry(root, width=300, height=40)
gender_combobox = ctk.CTkComboBox(root, values=["Male", "Female", "Other"], width=300, height=40)
country_entry = ctk.CTkEntry(root, width=300, height=40)
id_entry = ctk.CTkEntry(root, width=300, height=40)

# Profile picture and driving license image labels
profile_picture_label = ctk.CTkLabel(root, width=130, height=130)
driving_license_label = ctk.CTkLabel(root, width=130, height=130)

# Add blue rectangle (header) decoration
canvas.create_rectangle(0, 0, 1500, 320, fill="#1572D3", outline="")

# Layout for labels and entry fields
canvas.create_window(255, 370, window=ctk.CTkLabel(root, text="Username", font=("Poppins", 10)))
canvas.create_window(410, 420, window=username_entry)

canvas.create_window(840, 370, window=ctk.CTkLabel(root, text="Email", font=("Poppins", 10)))
canvas.create_window(1000, 420, window=email_entry)

canvas.create_window(245, 500, window=ctk.CTkLabel(root, text="Gender", font=("Poppins", 10)))
canvas.create_window(410, 550, window=gender_combobox)

canvas.create_window(840, 500, window=ctk.CTkLabel(root, text="Country", font=("Poppins", 10)))
canvas.create_window(1000, 550, window=country_entry)

canvas.create_window(850, 640, window=ctk.CTkLabel(root, text="ID Number", font=("Poppins", 10)))
canvas.create_window(1000, 690, window=id_entry)

# Display profile picture and driving license images
canvas.create_window(300, 220, window=profile_picture_label)
canvas.create_window(300, 690, window=driving_license_label)

# Buttons for uploading files
upload_profile_btn = ctk.CTkButton(root, text="Upload Profile Picture", command=upload_profile_picture)
canvas.create_window(490, 220, window=upload_profile_btn)

upload_license_btn = ctk.CTkButton(root, text="Upload Driving License", command=upload_driving_license)
canvas.create_window(490, 690, window=upload_license_btn)

# Edit and Save buttons
edit_btn = ctk.CTkButton(root, width=100, height=20, text="Edit", bg_color="#1572D3", text_color="white", font=("Arial", 12, "bold"), command=lambda: toggle_edit(True))
save_btn = ctk.CTkButton(root, width=100, height=20, text="Save", bg_color="#1572D3", text_color="white", font=("Arial", 12, "bold"), command=save_to_database)
canvas.create_window(1100, 300, window=edit_btn)
canvas.create_window(1250, 300, window=save_btn)

# Initialize UI
toggle_edit(False)  # Disable editing by default
load_user_data()  # Load the user's data into the fields


print(f"Profile Picture Path: {profile_picture_path}")
print(f"Driving License Path: {driving_license_path}")

root.mainloop()
