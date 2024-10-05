import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
from PIL import ImageTk, Image
from tkinter import messagebox
import subprocess
import os

# Functionality for the Search button
def search_action():
    location = location_entry.get()
    pickup_date = pickup_date_entry.get()
    return_date = return_date_entry.get()

    # Simple validation to ensure the fields are not empty
    if not location or not pickup_date or not return_date:
        messagebox.showwarning("Input Error", "Please fill all the fields.")
    else:
        print(f"Location: {location}, Pickup Date: {pickup_date}, Return Date: {return_date}")

# Function to open the selected button
def open_signin():
    root.destroy()
    subprocess.Popen(["python", "Login.py"])

# Function to open the script when the "How it Works" button is clicked
def open_howitworks():
    root.destroy()
    subprocess.Popen(["python", "How it Works.py"])

# Function to open the script when the "Become a Renter" button is clicked
def open_becomearenter():
    root.destroy()
    subprocess.Popen(["python", "Become a renter.py"])

# Create main application window
root = tk.Tk()
root.title("Car Rental Service")
root.geometry("1200x700")  # Adjust window size to fit the design

# Load and set the background image in the Home tab
background_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-10-05 232635.png"  # Your background image path
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

# create log in button
sign_in_button = tk.Button(root, bg="#1572D3", text="Sign In", font=("Poppins", 12), command=open_signin)
canvas.create_window(600, 40, anchor="nw", window=sign_in_button)


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


