import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
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

# Function to open the login script when the "Sign In" tab is clicked
def open_signin():
    login_script_path = r"C:\Users\User\OneDrive - student.newinti.edu.my\Carmala\main\Login.py"  # Path to the Login.py file
    os.system(f'python "{login_script_path}"')  # Execute the login script

# Create main application window
root = tk.Tk()
root.title("Car Rental Service")
root.geometry("1200x700")  # Adjust window size to fit the design

# Add a Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)  # Make the notebook fill the entire window

# Create frames for each tab
home_tab = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
sign_in_tab = ttk.Frame(notebook)

# Add the tabs
notebook.add(home_tab, text='Home')  # New Home tab
notebook.add(tab2, text='Become a Renter')
notebook.add(tab4, text='How It Works')
notebook.add(sign_in_tab, text='Sign In')  # Sign In tab

# Load and set the background image in the Home tab
background_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-20 133601.png"  # Your background image path
bg_image = Image.open(background_image_path)
bg_image = bg_image.resize((1200, 700), Image.LANCZOS)  # Resize to fit the window using LANCZOS filter
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to hold the background and other widgets in the Home tab
canvas = tk.Canvas(home_tab, width=1200, height=700)
canvas.pack(fill='both', expand=True)

# Add the background image to the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create input fields and labels for Location, Pickup Date, and Return Date at the bottom of the page
location_label = tk.Label(home_tab, text="Location", font=("Helvetica", 12), bg="white")
canvas.create_window(150, 600, anchor="nw", window=location_label)

location_entry = tk.Entry(home_tab, font=("Helvetica", 12), width=20)
canvas.create_window(230, 600, anchor="nw", window=location_entry)

pickup_label = tk.Label(home_tab, text="Pickup date", font=("Helvetica", 12), bg="white")
canvas.create_window(450, 600, anchor="nw", window=pickup_label)

pickup_date_entry = tk.Entry(home_tab, font=("Helvetica", 12), width=20)
canvas.create_window(540, 600, anchor="nw", window=pickup_date_entry)

return_label = tk.Label(home_tab, text="Return date", font=("Helvetica", 12), bg="white")
canvas.create_window(760, 600, anchor="nw", window=return_label)

return_date_entry = tk.Entry(home_tab, font=("Helvetica", 12), width=20)
canvas.create_window(850, 600, anchor="nw", window=return_date_entry)

# Create the search button
search_button = ttk.Button(home_tab, text="Search", command=search_action)
canvas.create_window(1070, 600, anchor="nw", window=search_button)

# Bind the event when "Sign In" tab is clicked
def on_tab_changed(event):
    selected_tab = event.widget.tab(event.widget.index("current"))["text"]
    if selected_tab == "Sign In":
        open_signin()

# Bind the event to the notebook
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# Start the Tkinter event loop
root.mainloop()
