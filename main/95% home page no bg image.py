import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
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
root.geometry("1280x1000")  # Adjust window size to fit the form and images

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

# Add a canvas to hold the scrollable content (the form and images)
canvas = tk.Canvas(home_tab, width=1280, height=1000)
canvas.pack(side=tk.LEFT, fill='both', expand=True)

# Add scrollbar to the canvas
scrollbar = ttk.Scrollbar(home_tab, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to add the scrollable content (form and images)
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

# Create the window for the scrollable frame inside the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Load and set the background image in the Home tab (directly onto the canvas)
background_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-20 133601.png"  # Your background image path
bg_image = Image.open(background_image_path)
bg_image = bg_image.resize((1280, 1000), Image.LANCZOS)  # Resize to fit the window using LANCZOS filter
bg_photo = ImageTk.PhotoImage(bg_image)

# Add the background image directly to the canvas (so it appears behind everything)
background_label = canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Ensure the canvas does not shrink to fit its content
canvas.pack_propagate(False)

# Keep a reference to the images globally to avoid garbage collection
image_refs = [bg_photo]

# Create input fields and labels for Location, Pickup Date, and Return Date on top of the background
location_label = tk.Label(scrollable_frame, text="Location", font=("Helvetica", 12), bg="white")
location_label.pack(pady=5)

location_entry = tk.Entry(scrollable_frame, font=("Helvetica", 12), width=20)
location_entry.pack(pady=5)

pickup_label = tk.Label(scrollable_frame, text="Pickup Date", font=("Helvetica", 12), bg="white")
pickup_label.pack(pady=5)

# Use a calendar date picker (DateEntry)
pickup_date_entry = DateEntry(scrollable_frame, font=("Helvetica", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
pickup_date_entry.pack(pady=5)

return_label = tk.Label(scrollable_frame, text="Return Date", font=("Helvetica", 12), bg="white")
return_label.pack(pady=5)

# Use a calendar date picker (DateEntry)
return_date_entry = DateEntry(scrollable_frame, font=("Helvetica", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
return_date_entry.pack(pady=5)

# Create the search button
search_button = ttk.Button(scrollable_frame, text="Search", command=search_action)
search_button.pack(pady=10)

# Load and display the two images you've uploaded INSIDE the scrollable frame
image1_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-28 205414.png"
image2_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-28 214731.png"

img1 = Image.open(image1_path)
img1 = img1.resize((1280, 780), Image.LANCZOS)  # Resize image to 1280x780
img1_photo = ImageTk.PhotoImage(img1)

img2 = Image.open(image2_path)
img2 = img2.resize((1280, 780), Image.LANCZOS)  # Resize image to 1280x780
img2_photo = ImageTk.PhotoImage(img2)

# Add the images to the scrollable frame, right after the form fields
label_img1 = tk.Label(scrollable_frame, image=img1_photo)
label_img1.pack(pady=0)  # No padding to connect images closely

label_img2 = tk.Label(scrollable_frame, image=img2_photo)
label_img2.pack(pady=0)  # No padding to connect images closely

# Store the images in the global image_refs list to avoid garbage collection
image_refs.extend([img1_photo, img2_photo])

# Bind the event when "Sign In" tab is clicked
def on_tab_changed(event):
    selected_tab = event.widget.tab(event.widget.index("current"))["text"]
    if selected_tab == "Sign In":
        open_signin()

# Bind the event to the notebook
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# Start the Tkinter event loop
root.mainloop()
