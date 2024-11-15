import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os
import subprocess
import sys
import Session

# Retrieve the logged-in user
user_data = Session.get_user_session()
if user_data:
    user_id = user_data["user_id"]
    print(f"Logged in as User ID: {user_id}")
else:
    print("No user is logged in.")


# Global variable for tracking the current page
current_page = 0
cars_per_page = 8  # Maximum number of car cards per page


# Function to open the selected button
def open_home():
    process = subprocess.Popen(["python", "Home.py"])
    print("Become a renter opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(400, root.destroy)  # Waits 300 milliseconds (1 second) before destroying

def get_available_cars(location, pickup_date, dropoff_date):
    try:
        conn = sqlite3.connect('Carmala.db')
        cursor = conn.cursor()

        # Convert to date only if pickup_date and dropoff_date are strings
        if isinstance(pickup_date, str):
            pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()
        if isinstance(dropoff_date, str):
            dropoff_date = datetime.strptime(dropoff_date, "%Y-%m-%d").date()

        # Fetch cars from CARTABLE that are available in the given location and date range
        cursor.execute('''
            SELECT c.CarID, c.CarName, c.CarLocation, c.CarCapacity, c.CarFueltype,
                   c.CarTransmission, c.CarFeatures, c.CarPrice, c.CarImage
            FROM CarList AS c
            LEFT JOIN Booking AS b ON c.CarID = b.CarID
            WHERE c.CarLocation = ?
              AND (b.PickupDate IS NULL OR b.DropoffDate IS NULL 
                   OR b.DropoffDate < ? OR b.PickupDate > ?)
        ''', (location, pickup_date, dropoff_date))

        available_cars = cursor.fetchall()
        conn.close()
        return available_cars
    except Exception as e:
        print(f"Error fetching cars: {e}")
        return []

# Functionality for the Search button
def search_action():
    location = location_entry.get().strip()  # Trim any leading/trailing spaces
    pickup_date = pickup_date_entry.get_date().strftime('%Y-%m-%d')
    return_date = return_date_entry.get_date().strftime('%Y-%m-%d')

    # Simple validation to ensure the fields are not empty
    # Simple validation to ensure the fields are not empty
    if not location or not pickup_date or not return_date:
        messagebox.showwarning("Input Error", "Please fill all the fields.")
    else:
        # Call get_available_cars with the correct arguments
        try:
            # Pass pickup_date_str and return_date_str directly
            available_cars = get_available_cars(location, pickup_date, return_date)
            if not available_cars:
                messagebox.showinfo("No Cars Available", f"No cars available in {location} during the selected dates.")
            else:
                # Call filter_car_data() to update car display based on new criteria
                filter_car_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open car list: {str(e)}")

# Global list to store selected cars for booking
booking_list = []

# Function to add a car to the booking list
def add_to_booking_list(car_data):
    car_id = car_data[0]  # CarID is assumed to be the first field
    if car_id not in [car[0] for car in booking_list]:  # check by CarID
        booking_list.append(car_data)
        messagebox.showinfo("Success", f"{car_data[1]} has been added to the booking list.")
    else:
        messagebox.showwarning("Already Added", f"{car_data[1]} is already in the booking list.")

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

    car_price = tk.Label(parent, text=f"RM{car_data[7]}/day", font=("Poppins", 12, 'bold'), bg="#F1F1F1")  # car_data[7] is CAR_PRICE
    car_price.grid(row=row+2, column=col, pady=5)

    car_attributes = tk.Label(parent, text=f"{car_data[5]} | {car_data[3]} seats | {car_data[4]}", font=("Poppins", 10), bg="#F1F1F1")
    car_attributes.grid(row=row+3, column=col, pady=5)

    # Rent Now Button
    add_booklist_button = tk.Button(parent, text="Add to Book List", font=("Poppins", 10, 'bold'), bg="#1572D3", fg="white", cursor="hand2",command=lambda: add_to_booking_list(car_data))
    add_booklist_button.grid(row=row+4, column=col, pady=10)

# Function to fetch car data from the database
def fetch_car_data(capacity_filter=None, transmission_filter=None, features_filter=None, price_filter=None, colour_filter=None, car_type_filter=None):
    connection = sqlite3.connect('Carmala.db')
    cursor = connection.cursor()

    # Construct the SQL query based on filters
    query = """
            SELECT * FROM CarList
            WHERE CarID NOT IN ( 
                SELECT CarID FROM Booking WHERE BookingStatus IN ('Pending', 'Approved')
            )
        """
    params = []

    if capacity_filter:
        query += " AND CarCapacity = ?"
        params.append(capacity_filter)

    if transmission_filter:
        query += " AND CarTransmission = ?"
        params.append(transmission_filter)

    if features_filter:
        query += " AND CarFeatures LIKE ?"
        params.append(f"%{features_filter}%")

    if price_filter:
        if " ~ " in price_filter:
            min_price, max_price = map(int, price_filter.split(' ~ '))
            query += " AND CarPrice BETWEEN ? AND ?"
            params.extend([min_price, max_price])
        elif ">" in price_filter:
            min_price = int(price_filter.replace('>', '').strip())
            query += " AND CarPrice >= ?"
            params.append(min_price)

    if colour_filter:
        query += " AND CarColour = ?"
        params.append(colour_filter)

    if car_type_filter:
        query += " AND CarType = ?"
        params.append(car_type_filter)

    cursor.execute(query, params)
    car_list = cursor.fetchall()

    connection.close()
    return car_list

# Function to filter and display car data based on selected criteria
def filter_car_data():
    global current_page
    current_page = 0  # Reset to the first page when new filter is applied
    display_cars()

# Function to display cars for the current page
# Update the display_cars function to handle the Colour filter
def display_cars():
    global current_page
    # Get selected filter values
    capacity_value = capacity_dropdown.get()
    transmission_value = transmission_dropdown.get()
    features_value = features_dropdown.get()
    price_value = price_dropdown.get()
    colour_value = colour_dropdown.get()
    car_type_value = car_type_dropdown.get()

    # Convert capacity to a numeric value
    capacity_filter = capacity_value.split()[0] if capacity_value else None

    # Fetch filtered car data
    filtered_cars = fetch_car_data(capacity_filter, transmission_value, features_value, price_value, colour_value, car_type_value)

    # Clear current car display
    for widget in car_frame.winfo_children():
        widget.destroy()

    # Calculate the start and end indices for the current page
    start_index = current_page * cars_per_page
    end_index = start_index + cars_per_page
    cars_on_page = filtered_cars[start_index:end_index]

    # Display cars for the current page
    for index, car_data in enumerate(cars_on_page):
        create_car_card(car_frame, (index // 4) * 5, index % 4, car_data)

    # Update page navigation buttons
    update_page_buttons(len(filtered_cars))

# Function to update the state of page navigation buttons
def update_page_buttons(total_cars):
    total_pages = (total_cars + cars_per_page - 1) // cars_per_page
    prev_button.config(state=tk.NORMAL if current_page > 0 else tk.DISABLED)
    next_button.config(state=tk.NORMAL if current_page < total_pages - 1 else tk.DISABLED)

    # Update page number display
    page_label.config(text=f"Page {current_page + 1} of {total_pages}")

# Function to go to the previous page
def previous_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        display_cars()

# Function to go to the next page
def next_page():
    global current_page
    current_page += 1
    display_cars()


# Function to open booking list with selectable cars
def open_booking_list(user_id, pickup_date, dropoff_date):
    # Initialize the booking list window
    booking_window = tk.Toplevel()
    booking_window.title("Booking List")
    booking_window.geometry("800x500")

    # Dictionary to track selected cars
    selected_cars = {}

    # Create a frame for the canvas and scrollbar
    frame_canvas = tk.Frame(booking_window)
    frame_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Create a canvas
    canvas = tk.Canvas(frame_canvas, bg="#F1F1F1")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to contain the car frames
    content_frame = tk.Frame(canvas, bg="#F1F1F1")
    content_frame_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Update the scrollregion each time the content changes
    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind the resize event to update the scrollregion
    content_frame.bind("<Configure>", update_scrollregion)

    # Enable scrolling with the mouse wheel
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    for car in booking_list:
        # Create a frame for each car
        car_frame = tk.Frame(content_frame, bg="#F1F1F1", relief=tk.RIDGE, borderwidth=2)
        car_frame.pack(padx=10, pady=10, fill=tk.X)

        # Load car image
        try:
            if os.path.exists(car[8]):  # car[8] is the image path
                car_image = Image.open(car[8])
                car_image = car_image.resize((200, 150), Image.LANCZOS)
                car_photo = ImageTk.PhotoImage(car_image)
            else:
                raise FileNotFoundError(f"File not found: {car[8]}")
        except Exception as e:
            print(f"Error loading image: {e}")
            # Placeholder image if the original is not found
            placeholder_image = Image.new('RGB', (200, 150), 'grey')
            car_photo = ImageTk.PhotoImage(placeholder_image)

        # Display the car image
        image_label = tk.Label(car_frame, image=car_photo, bg="#F1F1F1")
        image_label.image = car_photo  # Keep a reference to avoid garbage collection
        image_label.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

        # Display the car details on the right side
        car_name_label = tk.Label(car_frame, text=f"Name: {car[1]}", font=("Poppins", 12, 'bold'), bg="#F1F1F1")
        car_name_label.grid(row=0, column=1, sticky="w")

        car_location_label = tk.Label(car_frame, text=f"Location: {car[2]}", font=("Poppins", 10), bg="#F1F1F1")
        car_location_label.grid(row=1, column=1, sticky="w")

        car_capacity_label = tk.Label(car_frame, text=f"Capacity: {car[3]} seats", font=("Poppins", 10), bg="#F1F1F1")
        car_capacity_label.grid(row=2, column=1, sticky="w")

        car_fueltype_label = tk.Label(car_frame, text=f"Fuel Type: {car[4]}", font=("Poppins", 10), bg="#F1F1F1")
        car_fueltype_label.grid(row=3, column=1, sticky="w")

        car_transmission_label = tk.Label(car_frame, text=f"Transmission: {car[5]}", font=("Poppins", 10), bg="#F1F1F1")
        car_transmission_label.grid(row=4, column=1, sticky="w")

        car_features_label = tk.Label(car_frame, text=f"Features: {car[6]}", font=("Poppins", 10), bg="#F1F1F1")
        car_features_label.grid(row=5, column=1, sticky="w")

        car_price_label = tk.Label(car_frame, text=f"Price: RM{car[7]}/day", font=("Poppins", 12, 'bold'), bg="#F1F1F1")
        car_price_label.grid(row=6, column=1, sticky="w")

        # Add a checkbutton to select the car
        car_selected_var = tk.BooleanVar()  # Variable to track if car is selected
        select_checkbutton = tk.Checkbutton(car_frame, text="Select for Booking", variable=car_selected_var,
                                            bg="#F1F1F1")
        select_checkbutton.grid(row=0, column=2, sticky="e", padx=10)
        selected_cars[car[0]] = car_selected_var  # Track the selection state with CarID as key

        # Add a remove button with confirmation
        def remove_car(car_id, frame):
            if messagebox.askyesno("Remove Car", "Are you sure you want to remove this car from the booking list?"):
                frame.pack_forget()  # Hide the frame if removed
                selected_cars.pop(car_id, None)  # Remove from selected list if present

        remove_button = tk.Button(car_frame, text="Remove",
                                  command=lambda cid=car[0], frame=car_frame: remove_car(cid, frame),
                                  bg="#FF5C5C", fg="white")
        remove_button.grid(row=0, column=3, padx=10)

    # Confirm booking for selected cars
    def confirm_booking():
        # Collect selected car IDs
        selected_car_ids = [car_id for car_id, var in selected_cars.items() if var.get()]

        if not selected_car_ids:
            messagebox.showinfo("No Car Selected", "Please select at least one car to book.")
            return

        # Insert bookings into the Booking table
        conn = sqlite3.connect('Carmala.db')
        cursor = conn.cursor()

        for car_id in selected_car_ids:
            # Insert each booking, set status to 'Pending'
            cursor.execute("""
                INSERT INTO Booking (UserID, CarID, PickupDate, DropoffDate, BookingStatus)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, car_id, pickup_date, dropoff_date, 'Pending'))

        # Commit and close the database connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Booking Confirmed", "Your booking(s) have been submitted for approval.")
        booking_window.destroy()  # Close the booking window after confirmation

    # Add the Confirm Booking button
    confirm_button = tk.Button(booking_window, text="Confirm Booking", bg='#1572D3', fg='white', font=("Poppins", 12,"bold"), command=confirm_booking)
    confirm_button.pack(pady=10)



# Create main application window
root = tk.Tk()
root.title("Car List")
root.config(bg="white")
root.geometry("1120x700")

# Create a canvas to hold the background and other widgets in the Home tab
canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill='both', expand=True)

# Create the frame to hold the car cards
car_frame = tk.Frame(root, bg="#F1F1F1")
canvas.create_window(50, 120, anchor="nw", window=car_frame)

# Pagination controls
prev_button = tk.Button(root, text="Previous", command=previous_page)
next_button = tk.Button(root, text="Next", command=next_page)
page_label = tk.Label(root, text="Page 1 of 1", font=("Poppins", 12))

canvas.create_window(820, 610, anchor="nw", window=prev_button)
canvas.create_window(890, 610, anchor="nw", window=page_label)
canvas.create_window(1000, 610, anchor="nw", window=next_button)


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

# Retrieve command-line arguments
if len(sys.argv) == 4:
    location = sys.argv[1]
    pickup_date = sys.argv[2]
    return_date = sys.argv[3]
else:
    location = ""
    pickup_date = ""
    return_date = ""

# Display values or set them in Entry fields if needed
print(f"Location: {location}, Pickup Date: {pickup_date}, Return Date: {return_date}")

# Create input fields and labels for Location, Pickup Date, and Return Date
location_label = tk.Label(root, text="Location", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(170, 40, anchor="nw", window=location_label)

location_entry = tk.Entry(root, font=("Poppins", 12), width=20)
canvas.create_window(250, 40, anchor="nw", window=location_entry)
if location:
    location_entry.insert(0, location)

pickup_label = tk.Label(root, text="Pickup date", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(450, 40, anchor="nw", window=pickup_label)

pickup_date_entry = DateEntry(root, font=("Poppins", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(540, 40, anchor="nw", window=pickup_date_entry)
if pickup_date:
    # Convert pickup_date to a datetime.date object
    pickup_date_obj = datetime.strptime(pickup_date, '%Y-%m-%d').date()
    pickup_date_entry.set_date(pickup_date_obj)

return_label = tk.Label(root, text="Return date", font=("Poppins", 12), bg="#F1F1F1")
canvas.create_window(740, 40, anchor="nw", window=return_label)

return_date_entry = DateEntry(root, font=("Poppins", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(830, 40, anchor="nw", window=return_date_entry)
if return_date:
    # Convert return_date to a datetime.date object
    return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()
    return_date_entry.set_date(return_date_obj)

# Button to open booking list window with parameters passed
open_booking_button = tk.Button(root, text="Open Booking List", font=("Poppins", 12, 'bold'),
                                bg="#1572D3", fg="white", command=lambda: open_booking_list(user_id, pickup_date, return_date))
canvas.create_window(850, 447, anchor="nw", window=open_booking_button)


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

# Add Colour filter
colour_dropdown = create_dropdown("Colour", ["Red", "White", "Green", "Grey", "Black", "Yellow", "Silver"], 800, 260)

# Add the Car Type filter dropdown
car_type_dropdown = create_dropdown("Car Type", ["Sedan", "Hatchback", "SUV", "MPV", "Coupe", "Pickup"], 800, 290)

# Create the filter button
filter_button = tk.Button(root, text="Filter", command=filter_car_data, bg="#1572D3", fg="white", font=("Poppins", 10, 'bold'))
canvas.create_window(898, 325, anchor="nw", window=filter_button)

# Create the Back to home button
back_to_home_button = tk.Button(root, text="Back to home", bg="#1572D3", font=("Poppins",12,"bold"), fg="white", command=open_home)
canvas.create_window(872, 494, anchor="nw", window=back_to_home_button)

# Fetch and display all car data initially
filter_car_data()


# Run the main window
root.mainloop()
