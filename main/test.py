import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
import os
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
        filter_car_data()  # Trigger filtering when search is performed

# Function to create car display cards from database data
def create_car_card(parent, row, col, car_data):
    # Load car image
    try:
        if os.path.exists(car_data[8]):
            car_image = Image.open(car_data[8])  # car_data[8] is the CAR_IMAGE path
            car_image = car_image.resize((150, 100), Image.LANCZOS)
            car_photo = ImageTk.PhotoImage(car_image)
        else:
            raise FileNotFoundError(f"File not found: {car_data[8]}")
    except Exception as e:
        print(f"Error loading image: {e}")
        # Load a placeholder image if the original is not found
        placeholder_image = Image.new('RGB', (500, 200), 'grey')  # Create a grey placeholder
        car_photo = ImageTk.PhotoImage(placeholder_image)

    # Display the image
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
def fetch_car_data(capacity_filter=None, transmission_filter=None, features_filter=None, price_filter=None):
    connection = sqlite3.connect('Carmala.db')
    cursor = connection.cursor()

    # Construct the SQL query based on filters
    query = "SELECT * FROM CARTABLE WHERE 1=1"
    params = []

    if capacity_filter:
        query += " AND CAR_CAPACITY = ?"
        params.append(capacity_filter)

    if transmission_filter:
        query += " AND CAR_TRANSMISSION = ?"
        params.append(transmission_filter)

    if features_filter:
        query += " AND CAR_FEATURES LIKE ?"
        params.append(f"%{features_filter}%")

    if price_filter:
        # Handle different price ranges correctly
        if " ~ " in price_filter:
            min_price, max_price = map(int, price_filter.split(' ~ '))
            query += " AND CAR_PRICE BETWEEN ? AND ?"
            params.extend([min_price, max_price])
        elif ">" in price_filter:
            # Handle cases like ">1000" where the price is above a certain value
            min_price = int(price_filter.replace('>', '').strip())
            query += " AND CAR_PRICE >= ?"
            params.append(min_price)

    cursor.execute(query, params)
    car_list = cursor.fetchall()

    connection.close()
    return car_list


# Function to filter and display car data based on selected criteria
def filter_car_data():
    # Get selected filter values
    capacity_value = capacity_dropdown.get()
    transmission_value = transmission_dropdown.get()
    features_value = features_dropdown.get()
    price_value = price_dropdown.get()

    # Convert capacity to a numeric value
    capacity_filter = capacity_value.split()[0] if capacity_value else None

    # Fetch filtered car data
    filtered_cars = fetch_car_data(capacity_filter, transmission_value, features_value, price_value)

    # Clear current car display
    for widget in car_frame.winfo_children():
        widget.destroy()

    # Display filtered car data
    for index, car_data in enumerate(filtered_cars):
        create_car_card(car_frame, (index // 4) * 5, index % 4, car_data)

# Create main application window
root = tk.Tk()
root.title("Car List")
root.config(bg="#F1F1F1")
root.geometry("1120x700")

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
canvas.create_window(450, 40, anchor="nw", window=pickup_label)

pickup_date_entry = DateEntry(root, font=("Poppins", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(540, 40, anchor="nw", window=pickup_date_entry)

return_label = tk.Label(root, text="Return date", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(740, 40, anchor="nw", window=return_label)

return_date_entry = DateEntry(root, font=("Poppins", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(830, 40, anchor="nw", window=return_date_entry)

# Create the search button
search_button = ttk.Button(root, text="Search", command=search_action)
canvas.create_window(1030, 40, anchor="nw", window=search_button)

# Create the frame to hold the car cards
car_frame = tk.Frame(root, bg="#F1F1F1")
canvas.create_window(50, 120, anchor="nw", window=car_frame)

# Display label filter
filter_label = tk.Label(root, text="Filter", font=("Poppins", 14), bg="#F1F1F1")
canvas.create_window(900, 105, anchor="nw", window=filter_label)

# Function to create dropdown filters
def create_dropdown(label_text, options, x_offset, y_offset):
    label = tk.Label(root, text=label_text, font=("Poppins", 10), bg='#1572D3', fg='white', width=12)
    canvas.create_window(x_offset, y_offset, anchor="nw", window=label)

    dropdown = ttk.Combobox(root, font=("Poppins", 10), values=options, width=15)
    canvas.create_window(x_offset + 120, y_offset, anchor="nw", window=dropdown)
    return dropdown

# Capacity filter
capacity_dropdown = create_dropdown("Capacity", ["2 seats", "5 seats", "7 seats"], 800, 140)

# Transmission filter
transmission_dropdown = create_dropdown("Transmission", ["Automatic", "Manual"], 800, 170)

# Features filter
features_dropdown = create_dropdown("Features", ["Aircon", "4-Wheel drive", "Auto-steering"], 800, 200)

# Price filter
price_dropdown = create_dropdown("Price", ["0 ~ 200", "200 ~ 400", "400 ~ 600", "600 ~ 1000",">1000"], 800, 230)

# Fetch and display all car data initially
filter_car_data()

# Run the main window
root.mainloop()
