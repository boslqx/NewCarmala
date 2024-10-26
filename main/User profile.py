import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import sqlite3
import subprocess
import Session
import os

# Retrieve the logged-in user
user_data = Session.get_user_session()
if user_data:
    user_id = user_data["user_id"]
    print(f"Logged in as User ID: {user_id}")
else:
    print("No user is logged in.")



# Function to convert image file to BLOB (binary data)
def convert_image_to_blob(file_path):
    with open(file_path, 'rb') as file:
        blob_data = file.read()
    return blob_data


# Function to open the user profile window
def open_user_profile():
    if user_data:  # Ensure a user is logged in
        profile_window = tk.Tk()
        profile_window.title("User Profile")

        user_id = user_data["user_id"]

        # Fetch user details from the database using the logged_in_user's ID
        conn = sqlite3.connect('Carmala.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Email, Username, Gender, Country FROM UserAccount WHERE UserID = ?', (user_id,))
        user_details = cursor.fetchone()
        conn.close()

        if user_details:
            email = user_details[0]
            username = user_details[1]
            gender = user_details[2]
            country = user_details[3]

            # Display messagebox with username and email
            messagebox.showinfo("User Details", f"Username: {username}\nEmail: {email}")

            # Populate fields with the user's existing details
            username_entry.insert(0, username)
            email_entry.insert(0, email)
            gender_combobox.set(gender if gender else "Select Gender")
            country_entry.insert(0, country if country else "")

        else:
            messagebox.showerror("Error", "User details not found.")

        profile_window.mainloop()


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

# Function to open file dialog and select profile picture
def select_profile_picture():
    global profile_picture_path
    profile_picture_path = filedialog.askopenfilename(title="Select Profile Picture",
                                                      filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])


# Function to open file dialog and select driving license
def select_driving_license():
    global driving_license_path
    driving_license_path = filedialog.askopenfilename(title="Select Driving License", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])



# Create main application window
root = tk.Tk()
root.title(f"User Profile")
root.geometry("1100x700")  # Adjust window size to fit the design

# Add logo image to the canvas
canvas = tk.Canvas(root, width=1000, height=700)
canvas.pack(fill='both', expand=True)

# Add logo image to the canvas and make it a clickable button
logo_path = r"C:\Users\User\OneDrive\Pictures\Saved Pictures\cleaned_image.png"
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((150, 100), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)

# Place the image on the canvas
logo_button = tk.Label(root, image=logo_photo, cursor="hand2", bg="#F1F1F1")
canvas.create_window(10, 2, anchor="nw", window=logo_button)

# Bind the image to the open_home function
logo_button.bind("<Button-1>", lambda e: open_home())

# create become a renter button
become_renter_button = tk.Button(root, bg="#1572D3", text="Become a Renter", font=("Poppins", 12), command=open_becomearenter)
canvas.create_window(200, 40, anchor="nw", window=become_renter_button)

# create how it works button
how_it_works_button = tk.Button(root, bg="#1572D3", text="How It Works", font=("Poppins", 12), command=open_howitworks)
canvas.create_window(370, 40, anchor="nw", window=how_it_works_button)

# create user profile button
# create Booking details button
bookingdetails_button = tk.Button(root, bg="#1572D3", text="Booking Details", font=("Poppins", 12), command=open_bookingdetails)
canvas.create_window(510, 40, anchor="nw", window=bookingdetails_button)

# create Log out button
log_out_button = tk.Button(root, bg="#1572D3", text="Log Out", font=("Poppins", 12), command=log_out)
canvas.create_window(960, 40, anchor="nw", window=log_out_button)

# Add blue rectangle (header) decoration
canvas.create_rectangle(0, 120, 1500, 170, fill="#1572D3", outline="")

# Profile picture label
profile_pic_label = tk.Label(root, bg="#D9D9D9", cursor="hand2", width=20, height=10)
canvas.create_window(215, 230, window=profile_pic_label)
profile_pic_label.bind("<Button-1>", lambda e: select_profile_picture())

display_profilepic = tk.Label(root, text="Profile Picture", font=("Poppins",14))
canvas.create_window(350,190, window=display_profilepic)

# Username field
username_label = tk.Label(root, text="Username", font=("Poppins", 12))
canvas.create_window(200, 350, window=username_label)
username_entry = tk.Entry(root, width=40)
canvas.create_window(400, 350, window=username_entry)

# Email field
email_label = tk.Label(root, text="Email", font=("Poppins", 12))
canvas.create_window(700, 350, window=email_label)
email_entry = tk.Entry(root, width=40)
canvas.create_window(900, 350, window=email_entry)

# Gender combobox
gender_label = tk.Label(root, text="Gender", font=("Poppins", 12))
canvas.create_window(200, 420, window=gender_label)
gender_combobox = ttk.Combobox(root, values=["Male", "Female", "Others"], state="readonly", width=38)
gender_combobox.set("Select Gender")
canvas.create_window(400, 420, window=gender_combobox)

# Country field
country_label = tk.Label(root, text="Country", font=("Poppins", 12))
canvas.create_window(700, 420, window=country_label)
country_entry = tk.Entry(root, width=40)
canvas.create_window(900, 420, window=country_entry)

# Driving license upload
license_label = tk.Label(root, text="Driving License", font=("Poppins", 12))
canvas.create_window(180, 500, window=license_label)
upload_license_button = tk.Button(root, text="Upload picture", command=select_driving_license)
canvas.create_window(400, 500, window=upload_license_button)

# Identification number entry
id_label = tk.Label(root, text="Identification/Passport Number", font=("Poppins", 12))
canvas.create_window(660, 500, window=id_label)
id_entry = tk.Entry(root, width=40)
canvas.create_window(900, 500, window=id_entry)

# Save button
save_button = tk.Button(root, text="Save", width=10, height=2, command=save_to_database, bg="#1572D3", fg="white",
                        font=("Arial", 12, "bold"))
canvas.create_window(550, 600, window=save_button)

root.mainloop()
