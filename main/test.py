import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
from PIL import ImageTk, Image
from tkinter import messagebox
import subprocess
import sqlite3
from datetime import datetime


# get information from database about car available for renting
def get_available_cars(location, pickup_date, return_date):
    # Connect to the Carmala database
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    # Format dates to match database format (assuming they are stored as text)
    pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
    return_date = datetime.strptime(return_date, '%Y-%m-%d').date()

    # Query to get cars that are available in the specified location
    # and are not booked during the specified date range
    query = """
        SELECT * FROM CarList
        WHERE LOWER(CAR_LOCATION) = LOWER(?)
        AND CAR_ID NOT IN (
            SELECT CAR_ID FROM BookingHistory
            WHERE (pick_up_date <= ? AND drop_off_date >= ?)
        )
    """

    cursor.execute(query, (location, return_date, pickup_date))
    available_cars = cursor.fetchall()

    # Close the database connection
    conn.close()
    return available_cars

# Function to open the Car List interface with the selected parameters
def open_car_list(location, pickup_date, return_date):
    try:
        # Convert dates to string format for passing as arguments
        pickup_date_str = pickup_date.strftime('%Y-%m-%d')
        return_date_str = return_date.strftime('%Y-%m-%d')

        # Call the Car list.py script with the provided arguments
        root.destroy()
        subprocess.Popen(["python", "Car list.py", location, pickup_date_str, return_date_str])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Car List: {e}")

# Functionality for the Search button
def search_action():
    location = location_entry.get().strip()  # Trim any leading/trailing spaces
    pickup_date = pickup_date_entry.get_date()  # Get date object
    return_date = return_date_entry.get_date()  # Get date object

    # Simple validation to ensure the fields are not empty
    if not location or not pickup_date or not return_date:
        messagebox.showwarning("Input Error", "Please fill all the fields.")
    else:
        # Call get_available_cars with the correct arguments
        try:
            available_cars = get_available_cars(location, pickup_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d'))
            if not available_cars:
                messagebox.showinfo("No Cars Available", f"No cars available in {location} during the selected dates.")
            else:
                open_car_list(location, pickup_date, return_date)  # Proceed to open the Car List window
        except Exception as e:
            messagebox.showerror("Error", str(e))



# Function to open the selected button
def open_userprofile():
    root.destroy()
    subprocess.Popen(["python", "User profile.py"])

# Function to open the script when the "How it Works" button is clicked
def open_howitworks():
    root.destroy()
    subprocess.Popen(["python", "How it Works.py"])

# Function to open the script when the "Become a Renter" button is clicked
def open_becomearenter():
    root.destroy()
    subprocess.Popen(["python", "Become a renter.py"])


# Function to handle logout
def log_out():
    global logged_in_user
    logged_in_user = None  # Clear session
    root.destroy()
    subprocess.Popen(["python", "Login.py"])



# Create main application window
root = tk.Tk()
root.title("Car Rental Service")
root.geometry("1200x700")  # Adjust window size to fit the design

# Load and set the background image in the Home tab
background_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-10-17 095826.png"  # Your background image path
bg_image = Image.open(background_image_path)
bg_image = bg_image.resize((1200, 700), Image.LANCZOS)  # Resize to fit the window using LANCZOS filter
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to hold the background and other widgets in the Home tab
canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill='both', expand=True)

# Add the background image to the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# create become a renter button
become_renter_button = tk.Button(root, bg="#1572D3", text="Become a Renter", font=("Poppins", 12), command=open_becomearenter)
canvas.create_window(300, 40, anchor="nw", window=become_renter_button)

# create how it works button
how_it_works_button = tk.Button(root, bg="#1572D3", text="How It Works", font=("Poppins", 12), command=open_howitworks)
canvas.create_window(470, 40, anchor="nw", window=how_it_works_button)

# create user profile button
userprofile_button = tk.Button(root, bg="#1572D3", text="Profile", font=("Poppins", 12), command=open_userprofile)
canvas.create_window(610, 40, anchor="nw", window=userprofile_button)

# create log out button
logout_button = tk.Button(root, bg="#1572D3", text="Log Out", font=("Poppins", 12), command=log_out)
canvas.create_window(1100, 40, anchor="nw", window=logout_button)


# Create input fields and labels for Location, Pickup Date, and Return Date at the bottom of the page
location_label = tk.Label(root, text="Location", font=("Helvetica", 12), bg="white")
canvas.create_window(150, 600, anchor="nw", window=location_label)

location_entry = tk.Entry(root, font=("Helvetica", 12), width=20)
canvas.create_window(230, 600, anchor="nw", window=location_entry)

pickup_label = tk.Label(root, text="Pickup date", font=("Helvetica", 12), bg="white")
canvas.create_window(450, 600, anchor="nw", window=pickup_label)

# Replace the text entry with a calendar date picker (DateEntry)
pickup_date_entry = DateEntry(root, font=("Helvetica", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(540, 600, anchor="nw", window=pickup_date_entry)

return_label = tk.Label(root, text="Return date", font=("Helvetica", 12), bg="white")
canvas.create_window(760, 600, anchor="nw", window=return_label)

# Replace the text entry with a calendar date picker (DateEntry)
return_date_entry = DateEntry(root, font=("Helvetica", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(850, 600, anchor="nw", window=return_date_entry)

# Create the search button
search_button = ttk.Button(root, text="Search", command=search_action)
canvas.create_window(1070, 600, anchor="nw", window=search_button)


# Start the Tkinter event loop
root.mainloop()