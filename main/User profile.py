import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import sqlite3
from tkinter import filedialog
import subprocess
import tkinter as tk
import sqlite3

# Function to convert image file to BLOB (binary data)
def convert_image_to_blob(file_path):
    with open(file_path, 'rb') as file:
        blob_data = file.read()
    return blob_data

# Function to open file dialog and select profile picture
def select_profile_picture():
    global profile_picture_path
    profile_picture_path = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

# Function to open file dialog and select driving license
def select_driving_license():
    global driving_license_path
    driving_license_path = filedialog.askopenfilename(title="Select Driving License", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

# Function to open the user profile window
def open_user_profile():
    if logged_in_user:  # Ensure a user is logged in
        profile_window = tk.Tk()
        profile_window.title("User Profile")

        # Fetch user details from the database using the logged_in_user's ID
        conn = sqlite3.connect('Carmala.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Email, Username, Gender, Country FROM UserAccount WHERE UserID = ?', (logged_in_user[0],))
        user_details = cursor.fetchone()
        conn.close()

        # Display user profile information (username, email, gender, country)
        tk.Label(profile_window, text=f"Username: {user_details[1]}").pack()
        tk.Label(profile_window, text=f"Email: {user_details[0]}").pack()
        tk.Label(profile_window, text=f"Gender: {user_details[2]}").pack()
        tk.Label(profile_window, text=f"Country: {user_details[3]}").pack()

        # Logout button
        logout_button = tk.Button(profile_window, text="Logout", command=log_out)
        logout_button.pack()

        profile_window.mainloop()
    else:
        print("No user logged in")

# Function to log out and return to login window
def log_out():
    global logged_in_user
    logged_in_user = None  # Clear session
    root.destroy()
    open_login()

def open_login():
    subprocess.Popen(["python", "Login.py"])

# Function to open the selected button
def open_home():
    root.destroy()
    subprocess.Popen(["python", "Home.py"])

# Function to open the script when the "How it Works" button is clicked
def open_howitworks():
    root.destroy()
    subprocess.Popen(["python", "How it Works.py"])

# Function to open the script when the "Become a Renter" button is clicked
def open_becomearenter():
    root.destroy()
    subprocess.Popen(["python", "Become a renter.py"])

# Function to open the selected button
def open_userprofile():
    root.destroy()
    subprocess.Popen(["python", "User profile.py"])

# Function to allow users to upload their profile picture
def upload_profile_picture():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image = image.resize((150, 100), Image.LANCZOS)
        profile_photo = ImageTk.PhotoImage(image)
        profile_pic_label.config(image=profile_photo)
        profile_pic_label.image = profile_photo

# Function to upload the driving license image
def upload_license():
    filedialog.askopenfilename()

# Function to save user data to the database
def save_to_database(user_id):
    username = username_entry.get()
    email = email_entry.get()  # This can still be updated if needed
    gender = gender_combobox.get()
    country = country_combobox.get()
    identification_number = id_entry.get()

    # Assuming you have functions or logic to handle image file selection and conversion
    profile_picture = convert_image_to_blob(profile_picture_path.get())  # Replace with the actual path or logic
    driving_license = convert_image_to_blob(driving_license_path.get())  # Replace with the actual path or logic

    # Open the connection to the database
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    # Ensure the table exists (if it doesn't, create it)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserAccount (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT NOT NULL UNIQUE,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL,
            ProfilePicture BLOB,
            Gender TEXT,
            Country TEXT,
            DrivingLicense BLOB,
            IdentificationNumber TEXT
        )
    ''')

    # Update the user's data, including profile picture and driving license
    cursor.execute('''
        UPDATE UserAccount
        SET Username = ?, Email = ?, Gender = ?, Country = ?, IdentificationNumber = ?, ProfilePicture = ?, DrivingLicense = ?
        WHERE UserID = ?
    ''', (username, email, gender, country, identification_number, profile_picture, driving_license, user_id))

    conn.commit()  # Commit the changes
    conn.close()   # Close the database connection

    print("User profile updated successfully!")



# Create main application window
root = tk.Tk()
root.title("User Profile")
root.geometry("1100x700")  # Adjust window size to fit the design

# Create a canvas to hold the background and other widgets in the Home tab
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
userprofile_button = tk.Button(root, bg="#1572D3", text="Profile", font=("Poppins", 12), command=open_userprofile)
canvas.create_window(510, 40, anchor="nw", window=userprofile_button)

# create Log out button
log_out_button = tk.Button(root, bg="#1572D3", text="Log Out", font=("Poppins", 12), command=log_out)
canvas.create_window(960, 40, anchor="nw", window=log_out_button)

# Add blue rectangle (header) decoration
canvas.create_rectangle(0, 120, 1500, 170, fill="#1572D3", outline="")

# Profile picture label
profile_pic_label = tk.Label(root, bg="#D9D9D9", cursor="hand2", width=10, height=5)
canvas.create_window(215, 230, window=profile_pic_label)

# Bind the profile picture label to the upload function
profile_pic_label.bind("<Button-1>", lambda e: upload_profile_picture())

# Change or update username
username_label = tk.Label(root, text="Username", font=("Poppins", 12))
canvas.create_window(200, 350, window=username_label)

username_entry = tk.Entry(root, width=40)
canvas.create_window(400, 350, window=username_entry)

# Change or update email
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

# Country combobox (Asia countries only)
country_label = tk.Label(root, text="Country", font=("Arial", 12))
canvas.create_window(700, 420, window=country_label)

country_combobox = ttk.Combobox(root, values=["Malaysia","Indonesia","Thailand","Brunei","China", "India", "Japan", "Singapore", "South Korea"], state="readonly", width=38)
country_combobox.set("Select Country")
canvas.create_window(900, 420, window=country_combobox)

# Upload driving license
license_label = tk.Label(root, text="Driving License/International License", font=("Poppins", 12))
canvas.create_window(180, 500, window=license_label)

upload_license_button = tk.Button(root, text="Upload picture", command=upload_license)
canvas.create_window(400, 500, window=upload_license_button)

# Identification number entry
id_label = tk.Label(root, text="Identification/Passport Number", font=("Poppins", 12))
canvas.create_window(660, 500, window=id_label)

id_entry = tk.Entry(root, width=40)
canvas.create_window(900, 500, window=id_entry)

# Save button (styled and positioned correctly)
save_button = tk.Button(root, text="Save", width=10, height=2, command=save_to_database, bg="#1572D3", fg="white", font=("Arial", 12, "bold"))
canvas.create_window(550, 600, window=save_button)

root.mainloop()