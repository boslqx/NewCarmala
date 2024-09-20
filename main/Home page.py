import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox

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
root.title("Car Rental Service")
root.geometry("1200x700")  # Adjust window size to fit the design

# Add a Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)  # Make the notebook fill the entire window

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)

# Add the tabs
notebook.add(tab1, text='Become a Renter')
notebook.add(tab2, text='Rental Deals')
notebook.add(tab3, text='How It Works')
notebook.add(tab4, text='Why Choose Us')
notebook.add(tab5, text='Sign In')

# Load and set the background image in the main tab (tab1)
background_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-20 133601.png"  # Your background image path
bg_image = Image.open(background_image_path)
bg_image = bg_image.resize((1200, 700), Image.LANCZOS)  # Resize to fit the window using LANCZOS filter
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to hold the background and other widgets
canvas = tk.Canvas(tab1, width=1200, height=700)
canvas.pack(fill='both', expand=True)

# Add the background image to the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create the 'Find, Book, and Rent a Car' label (at the top)
title_label = tk.Label(tab1, text="Find, book and rent a car Easily", font=("Helvetica", 30, "bold"), bg="white", fg="black")
canvas.create_window(50, 120, anchor="nw", window=title_label)

subtitle_label = tk.Label(tab1, text="Get a car wherever and whenever you need it with your iOS and Android device.", font=("Helvetica", 14), bg="white", fg="black")
canvas.create_window(50, 180, anchor="nw", window=subtitle_label)

# Create input fields and labels for Location, Pickup Date, and Return Date at the bottom of the page
location_label = tk.Label(tab1, text="Location", font=("Helvetica", 12), bg="white")
canvas.create_window(150, 600, anchor="nw", window=location_label)

location_entry = tk.Entry(tab1, font=("Helvetica", 12), width=20)
canvas.create_window(230, 600, anchor="nw", window=location_entry)

pickup_label = tk.Label(tab1, text="Pickup date", font=("Helvetica", 12), bg="white")
canvas.create_window(450, 600, anchor="nw", window=pickup_label)

pickup_date_entry = tk.Entry(tab1, font=("Helvetica", 12), width=20)
canvas.create_window(540, 600, anchor="nw", window=pickup_date_entry)

return_label = tk.Label(tab1, text="Return date", font=("Helvetica", 12), bg="white")
canvas.create_window(760, 600, anchor="nw", window=return_label)

return_date_entry = tk.Entry(tab1, font=("Helvetica", 12), width=20)
canvas.create_window(850, 600, anchor="nw", window=return_date_entry)

# Create the search button
search_button = ttk.Button(tab1, text="Search", command=search_action)
canvas.create_window(1070, 600, anchor="nw", window=search_button)

# Start the Tkinter event loop
root.mainloop()

