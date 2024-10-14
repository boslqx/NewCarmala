import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
import subprocess

# Function to open the selected button
def open_home():
    root.destroy()
    subprocess.Popen(["python", "Home.py"])

# Functionality for the Search button
def search_action():
    location = location_entry.get()
    pickup_date = pickup_date_entry.get()
    return_date = return_date_entry.get()

    if not location or not pickup_date or not return_date:
        messagebox.showwarning("Input Error", "Please fill all the fields.")
    else:
        print(f"Location: {location}, Pickup Date: {pickup_date}, Return Date: {return_date}")

# Function to create car display cards from database data
def create_car_card(parent, row, col, car_data):
    # Load car image
    try:
        car_image = Image.open(car_data[8])  # car_data[8] is the CAR_IMAGE path
        car_image = car_image.resize((500, 500), Image.LANCZOS)
        car_photo = ImageTk.PhotoImage(car_image)
    except Exception as e:
        car_photo = None

    image_placeholder = tk.Label(parent, image=car_photo, bg="grey")
    image_placeholder.image = car_photo  # Keep a reference to avoid garbage collection
    image_placeholder.grid(row=row, column=col, padx=10, pady=10)

    # Display car details
    car_name = tk.Label(parent, text=car_data[1], font=("Poppins", 12), bg="#F1F1F1")  # car_data[1] is CAR_NAME
    car_name.grid(row=row+1, column=col, pady=5)

    car_price = tk.Label(parent, text=f"${car_data[7]}/day", font=("Poppins", 12, 'bold'), bg="#F1F1F1")  # car_data[7] is CAR_PRICE
    car_price.grid(row=row+2, column=col, pady=5)

    car_attributes = tk.Label(parent, text=f"{car_data[5]} | {car_data[3]} seats | {car_data[4]}", font=("Poppins", 10), bg="#F1F1F1")
    car_attributes.grid(row=row+3, column=col, pady=5)

    # Rent Now Button
    add_booklist_button = tk.Button(parent, text="Add to Book List", font=("Poppins", 10, 'bold'), bg="#1572D3", fg="white", cursor="hand2")
    add_booklist_button.grid(row=row+4, column=col, pady=10)

# Function to fetch car data from the database
def fetch_car_data():
    connection = sqlite3.connect('Carmala.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM CARTABLE")
    car_list = cursor.fetchall()

    connection.close()
    return car_list

# Create main application window
root = tk.Tk()
root.title("Car List")
root.config(bg="#F1F1F1")
root.geometry("1200x700")

# Create a canvas to hold the background and other widgets in the Home tab
canvas = tk.Canvas(root, width=1200, height=700)
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

# Create input fields and labels for Location, Pickup Date, and Return Date
location_label = tk.Label(root, text="Location", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(170, 40, anchor="nw", window=location_label)

location_entry = tk.Entry(root, font=("Poppins", 12), width=20)
canvas.create_window(250, 40, anchor="nw", window=location_entry)

pickup_label = tk.Label(root, text="Pickup date", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(470, 40, anchor="nw", window=pickup_label)

pickup_date_entry = DateEntry(root, font=("Poppins", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(560, 40, anchor="nw", window=pickup_date_entry)

return_label = tk.Label(root, text="Return date", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(760, 40, anchor="nw", window=return_label)

return_date_entry = DateEntry(root, font=("Poppins", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(850, 40, anchor="nw", window=return_date_entry)

# Create the search button
search_button = ttk.Button(root, text="Search", command=search_action)
canvas.create_window(1070, 40, anchor="nw", window=search_button)

# Create the frame to hold the car cards
car_frame = tk.Frame(root, bg="#F1F1F1")
canvas.create_window(50, 160, anchor="nw", window=car_frame)

# Fetch and display car data from the database
car_data_list = fetch_car_data()
for index, car_data in enumerate(car_data_list):
    create_car_card(car_frame, (index // 4) * 5, index % 4, car_data)  # 2 rows and 4 columns

# Run the main window
root.mainloop()
