import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
from PIL import ImageTk, Image
from tkinter import messagebox
import subprocess
import os

# Function to open the selected button
def open_home():
    root.destroy()
    subprocess.Popen(["python", "Home.py"])

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

# Create main application window
root = tk.Tk()
root.title("Car list")
root.config(bg="#F1F1F1")
root.geometry("1200x700")  # Adjust window size to fit the design

# Create a canvas to hold the background and other widgets in the Home tab
canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill='both', expand=True)

# Add logo image to the canvas and make it a clickable button
logo_path = r"C:\Users\User\OneDrive\Pictures\Saved Pictures\cleaned_image.png"  # Path to your image
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((150, 100), Image.LANCZOS)  # Resize as needed
logo_photo = ImageTk.PhotoImage(logo_img)

# Place the image on the canvas
logo_button = tk.Label(root, image=logo_photo, cursor="hand2", bg="#F1F1F1")  # Set cursor to hand2 for clickable feel
canvas.create_window(10, 2, anchor="nw", window=logo_button)

# Bind the image to the open_home function
logo_button.bind("<Button-1>", lambda e: open_home())

# Create input fields and labels for Location, Pickup Date, and Return Date at the bottom of the page
location_label = tk.Label(root, text="Location", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(170, 40, anchor="nw", window=location_label)

location_entry = tk.Entry(root, font=("Poppins", 12), width=20)
canvas.create_window(250, 40, anchor="nw", window=location_entry)

pickup_label = tk.Label(root, text="Pickup date", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(470, 40, anchor="nw", window=pickup_label)

# Replace the text entry with a calendar date picker (DateEntry)
pickup_date_entry = DateEntry(root, font=("Poppins", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(560, 40, anchor="nw", window=pickup_date_entry)

return_label = tk.Label(root, text="Return date", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(760, 40, anchor="nw", window=return_label)

# Replace the text entry with a calendar date picker (DateEntry)
return_date_entry = DateEntry(root, font=("Poppins", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(850, 40, anchor="nw", window=return_date_entry)

# Create the search button
search_button = ttk.Button(root, text="Search", command=search_action)
canvas.create_window(1070, 40, anchor="nw", window=search_button)

# Add filter dropdowns below the logo

# Function to create dropdown filters
def create_dropdown(label_text, options, x_offset, y_offset):
    label = tk.Label(root, text=label_text, font=("Poppins", 10), bg='#1572D3', fg='white', width=12)
    canvas.create_window(x_offset, y_offset, anchor="nw", window=label)

    dropdown = ttk.Combobox(root, font=("Poppins", 10), values=options, width=15)
    canvas.create_window(x_offset + 120, y_offset, anchor="nw", window=dropdown)

# Capacity filter (adjust y_offset to 100)
create_dropdown("Capacity", ["Any","2 seats", "4 seats", "5 seats", "6 seats"], 100, 100)

# Transmission filter (adjust y_offset to 100)
create_dropdown("Transmission", ["Any","Automatic", "Manual"], 360, 100)

# Features filter (adjust y_offset to 100)
create_dropdown("Features", ["Any","Aircon", "4-Wheel drive", "Auto-steering"], 630, 100)

# Price filter (adjust y_offset to 100)
create_dropdown("Price", ["Any","0 ~ 200", "200 ~ 400", "400 ~ 600", "600 ~ 1000", "1000 ~"], 890, 100)


# Run the main window
root.mainloop()
