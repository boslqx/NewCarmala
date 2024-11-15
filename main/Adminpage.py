import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import os
from datetime import datetime


# Global variable to store logged-in admin
logged_in_admin = None


# Function to open the admin page (replace with actual home page code)
def open_admin_page():
    # Debug print to verify admin details
    if logged_in_admin:
        print(f"Logged in admin details: {logged_in_admin}")
    else:
        print("No admin is currently logged in.")

    os.system('python Adminpage.py')  # This will execute the Adminpage.py script


# Example of how to use the logged-in admin information
def show_admin_info():
    if logged_in_admin:
        print(f"Logged in as: {logged_in_admin[1]}")  # Example of accessing the admin name
    else:
        print("No admin is currently logged in.")

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check if the user is admin or regular user
    if username == "admin" and password == "adminpass":
        open_admin_panel()
    elif username == "user" and password == "pass":
        messagebox.showinfo("Login Successful", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")


# Function to open the admin panel
def open_admin_panel():
    # Hide the login frame and display the admin panel
    login_frame.pack_forget()
    admin_frame.pack(fill=tk.BOTH, expand=True)

    # Remove the right side image (used in login page)
    right_frame.pack_forget()

    # Load and set admin-specific image background
    admin_image_path = r"C:\Users\User\Downloads\Group 2.png"  # Add your path
    admin_image = Image.open(admin_image_path)
    admin_image = admin_image.resize((1280, 780), Image.LANCZOS)
    admin_photo = ImageTk.PhotoImage(admin_image)
    admin_image_label.config(image=admin_photo)
    admin_image_label.image = admin_photo  # Keep reference to avoid garbage collection

    # Position buttons on the admin panel
    place_buttons_on_image()


# Function to place buttons in the admin panel
def place_buttons_on_image():
    # Side panel buttons
    button_statistics.place(x=65, y=155, width=180, height=40)
    button_pending_bookings.place(x=65, y=205, width=180, height=40)
    button_feedback.place(x=65, y=255, width=180, height=40)
    button_manage_cars.place(x=65, y=305, width=180, height=40)
    button_agencies.place(x=65, y=355, width=180, height=40)
    button_settings.place(x=65, y=405, width=180, height=40)


# Function to display car availability data
def display_car_availability():
    admin_frame.pack_forget()  # Hide admin panel
    car_availability_frame.pack(fill=tk.BOTH, expand=True)  # Show the car availability frame

    # Clear previous entries from Car Treeview
    for row in car_tree.get_children():
        car_tree.delete(row)

    # Fetch data from the database
    conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")  # Replace with your actual DB path
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CarList")  # Adjust the query to match your table structure
    rows = cursor.fetchall()

    # Insert data into the Car Treeview
    for row in rows:
        car_tree.insert("", tk.END, values=row)

    conn.close()


def display_agencies_frame():
    admin_frame.pack_forget()  # Hide admin panel
    agencies_frame.pack(fill=tk.BOTH, expand=True)  # Show the agencies frame

    # Clear previous entries from Agency Treeview
    for row in agency_tree.get_children():
        agency_tree.delete(row)

    # Fetch data from the database
    conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")  # Replace with your actual DB path
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM AdminAccount")  # Adjust the query to match your table structure
    rows = cursor.fetchall()

    # Insert data into the Agency Treeview
    for row in rows:
        agency_tree.insert("", tk.END, values=row)

    conn.close()

def delete_selected_row():
        # Get selected item from Treeview
        selected_item = car_tree.selection()

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a row to delete.")
            return

        # Get the car_id (or the primary key) from the selected row
        selected_car = car_tree.item(selected_item)['values']  # Get the values from the selected row
        car_id = selected_car[0]  # Assuming the car_id is the first column

        # Confirm the deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Car ID {car_id}?")
        if confirm:
            try:
                # Delete from the database
                conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM CarList WHERE CarID=?",
                               (CarID,))  # Adjust if your primary key has a different name
                conn.commit()
                conn.close()

                # Delete the row from the Treeview
                car_tree.delete(selected_item)

                messagebox.showinfo("Success", f"Car ID {car_id} has been deleted successfully.")

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showinfo("Cancelled", "Deletion cancelled.")
def delete_selected_agency():
    # Get selected item from Treeview
    selected_item = agency_tree.selection()

    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a row to delete.")
        return

    # Get the admin_id (or the primary key) from the selected row
    selected_agency = agency_tree.item(selected_item)['values']  # Get the values from the selected row
    AdminID = selected_agency[0]  # Assuming the admin_id is the first column

    # Confirm the deletion
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Admin ID {AdminID}?")
    if confirm:
        try:
            # Delete from the database
            conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")  # Replace with your actual database path
            cursor = conn.cursor()
            cursor.execute("DELETE FROM AdminAccount WHERE AdminID=?", (AdminID,))  # Adjust to match your table structure
            conn.commit()
            conn.close()

            # Delete the row from the Treeview
            agency_tree.delete(selected_item)

            messagebox.showinfo("Success", f"Admin ID {AdminID} has been deleted successfully.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showinfo("Cancelled", "Deletion cancelled.")
def open_add_agency_form():
    # Create a new window
    add_window = tk.Toplevel()
    add_window.title("Add New Agency")
    add_window.geometry('400x400')

    # Labels and entry fields for new agency details
    tk.Label(add_window, text="Admin ID").pack(pady=5)
    entry_admin_id = tk.Entry(add_window)
    entry_admin_id.pack(pady=5)

    tk.Label(add_window, text="Admin Username").pack(pady=5)
    entry_admin_username = tk.Entry(add_window)
    entry_admin_username.pack(pady=5)

    tk.Label(add_window, text="Admin Password").pack(pady=5)
    entry_admin_password = tk.Entry(add_window)
    entry_admin_password.pack(pady=5)

    tk.Label(add_window, text="Admin Email").pack(pady=5)
    entry_admin_email = tk.Entry(add_window)
    entry_admin_email.pack(pady=5)

    # Add button to save the new agency
    tk.Button(add_window, text="Add Agency", command=lambda: add_new_agency(entry_admin_id.get(), entry_admin_username.get(), entry_admin_password.get(), entry_admin_email.get(), add_window)).pack(pady=20)

def add_new_agency(AdminID, AdminUsername, AdminPassword, AdminEmail, add_window):
    # Check if any of the fields are empty
    if not AdminID or not AdminUsername or not AdminPassword or not AdminEmail:
        messagebox.showwarning("Input Error", "All fields must be filled.")
        return

    try:
        # Insert new agency into the database
        conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")  # Replace with your actual DB path
        cursor = conn.cursor()
        cursor.execute("INSERT INTO AdminAccount (AdminID, AdminUsername, AdminPassword, AdminEmail) VALUES (?, ?, ?, ?)",
                       (AdminID, AdminUsername, AdminPassword, AdminEmail))
        conn.commit()
        conn.close()

        # Insert the new agency into the Treeview
        agency_tree.insert("", tk.END, values=(AdminID, AdminUsername, AdminPassword, AdminEmail))

        # Close the Add Agency window
        add_window.destroy()

        messagebox.showinfo("Success", "New agency has been added successfully.")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


def open_add_car_form():
    # Create a new window for adding car details
    add_car_window = tk.Toplevel(root)
    add_car_window.title("Add New Car")
    add_car_window.geometry("600x600")

    # Create form labels and entry fields for car details
    tk.Label(add_car_window, text="Car Name:").pack(pady=5)
    entry_car_name = tk.Entry(add_car_window)
    entry_car_name.pack(pady=5)

    tk.Label(add_car_window, text="Car Location:").pack(pady=5)
    entry_car_location = tk.Entry(add_car_window)
    entry_car_location.pack(pady=5)

    tk.Label(add_car_window, text="Car Capacity:").pack(pady=5)
    entry_car_capacity = tk.Entry(add_car_window)
    entry_car_capacity.pack(pady=5)

    tk.Label(add_car_window, text="Car Fuel Type:").pack(pady=5)
    entry_car_fueltype = tk.Entry(add_car_window)
    entry_car_fueltype.pack(pady=5)

    tk.Label(add_car_window, text="Car Transmission:").pack(pady=5)
    entry_car_transmission = tk.Entry(add_car_window)
    entry_car_transmission.pack(pady=5)

    tk.Label(add_car_window, text="Car Features:").pack(pady=5)
    entry_car_features = tk.Entry(add_car_window)
    entry_car_features.pack(pady=5)

    tk.Label(add_car_window, text="Car Price:").pack(pady=5)
    entry_car_price = tk.Entry(add_car_window)
    entry_car_price.pack(pady=5)

    tk.Label(add_car_window, text="Car Image URL:").pack(pady=5)
    entry_car_image = tk.Entry(add_car_window)
    entry_car_image.pack(pady=5)

    # Submit button to add car
    submit_button = tk.Button(add_car_window, text="Add Car", command=lambda: add_car(entry_car_name.get(),entry_car_location.get(),entry_car_capacity.get(), entry_car_fueltype.get(),entry_car_transmission.get(),entry_car_features.get(),entry_car_price.get(),entry_car_image.get(),add_car_window))
    submit_button.pack(pady=20)

def logout():
    root.destroy()  # Close the admin panel window
    os.system('python "C:\\Users\\User\\Downloads\\Carmala\\main\\login.py"')  # Reopen the login screen


def add_car(name, location, capacity, fueltype, transmission, features, price, image_url, window):
    if not all([name, location, capacity, fueltype, transmission, features, price, image_url]):
        messagebox.showerror("Error", "All fields must be filled out!")
        return

    try:
        conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")
        cursor = conn.cursor()

        # Insert new car details into CarList (adjust table/column names as necessary)
        cursor.execute("""
            INSERT INTO CarList (CarName, CarLocation, CarCapacity, CarFueltype, CarTransmission, CarFeatures, CarPrice, CarImage, AdminID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        name, location, capacity, fueltype, transmission, features, price, image_url, 1))  # Adjust `admin_id` if needed

        conn.commit()

        # Insert new car into Treeview
        car_tree.insert("", tk.END, values=(
        cursor.lastrowid, name, location, capacity, fueltype, transmission, features, price, image_url, 1))

        messagebox.showinfo("Success", "Car added successfully!")
        window.destroy()  # Close the add car window after submission

    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()


def open_edit_car_form():
    # Get selected car from the Treeview
    selected_item = car_tree.selection()
    if not selected_item:
        messagebox.showwarning("Edit Car", "Please select a car to edit.")
        return

    # Get the car data
    car_data = car_tree.item(selected_item)['values']

    if not car_data:
        messagebox.showwarning("Edit Car", "Could not retrieve car data.")
        return

    # Create a new window for editing car details
    edit_car_window = tk.Toplevel(root)
    edit_car_window.title("Edit Car")
    edit_car_window.geometry("600x600")

    # Create form labels and entry fields pre-filled with the selected car data
    tk.Label(edit_car_window, text="Car Name:").pack(pady=5)
    entry_car_name = tk.Entry(edit_car_window, width=40)
    entry_car_name.pack(pady=5)
    entry_car_name.insert(0, car_data[1])

    tk.Label(edit_car_window, text="Car Location:").pack(pady=5)
    entry_car_location = tk.Entry(edit_car_window, width=40)
    entry_car_location.pack(pady=5)
    entry_car_location.insert(0, car_data[2])

    tk.Label(edit_car_window, text="Car Capacity:").pack(pady=5)
    entry_car_capacity = tk.Entry(edit_car_window, width=40)
    entry_car_capacity.pack(pady=5)
    entry_car_capacity.insert(0, car_data[3])

    tk.Label(edit_car_window, text="Car Fuel Type:").pack(pady=5)
    entry_car_fueltype = tk.Entry(edit_car_window, width=40)
    entry_car_fueltype.pack(pady=5)
    entry_car_fueltype.insert(0, car_data[4])

    tk.Label(edit_car_window, text="Car Transmission:").pack(pady=5)
    entry_car_transmission = tk.Entry(edit_car_window, width=40)
    entry_car_transmission.pack(pady=5)
    entry_car_transmission.insert(0, car_data[5])

    tk.Label(edit_car_window, text="Car Features:").pack(pady=5)
    entry_car_features = tk.Entry(edit_car_window, width=40)
    entry_car_features.pack(pady=5)
    entry_car_features.insert(0, car_data[6])

    tk.Label(edit_car_window, text="Car Price:").pack(pady=5)
    entry_car_price = tk.Entry(edit_car_window, width=40)
    entry_car_price.pack(pady=5)
    entry_car_price.insert(0, car_data[7])

    tk.Label(edit_car_window, text="Car Image URL:").pack(pady=5)
    entry_car_image = tk.Entry(edit_car_window, width=40)
    entry_car_image.pack(pady=5)
    entry_car_image.insert(0, car_data[8])

    # Submit button to update car details
    submit_button = tk.Button(edit_car_window, text="Save Changes", command=lambda: edit_car(car_data[0], # car_id
                                                                                             entry_car_name.get(),
                                                                                             entry_car_location.get(),
                                                                                             entry_car_capacity.get(),
                                                                                             entry_car_fueltype.get(),
                                                                                             entry_car_transmission.get(),
                                                                                             entry_car_features.get(),
                                                                                             entry_car_price.get(),
                                                                                             entry_car_image.get(),
                                                                                             edit_car_window))
    submit_button.pack(pady=20)


def edit_car(car_id, name, location, capacity, fueltype, transmission, features, price, image, window):
    # Update the car details in the database
    conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")  # Replace with your actual DB path
    cursor = conn.cursor()

    # Execute update query
    cursor.execute("""
        UPDATE CarList SET 
        CarName = ?, CarLocation = ?, CarCapacity = ?, CarFueltype = ?, CarTransmission = ?, 
        CarFeatures = ?,CarPrice = ?,CarImage = ?
        WHERE CarID= ?
    """, (name, location, capacity, fueltype, transmission, features, price, image, car_id))

    conn.commit()
    conn.close()

    # Refresh the car tree view after update
    display_car_availability()

    # Close the edit car window
    window.destroy()

    messagebox.showinfo("Edit Car", "Car details updated successfully.")

def display_booking_history():
    admin_frame.pack_forget()  # Hide admin panel
    booking_history_frame.pack(fill=tk.BOTH, expand=True)  # Show booking history frame

    # Clear previous entries from Booking Treeview
    for row in booking_tree.get_children():
        booking_tree.delete(row)

    # Fetch data from the database
    conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")  # Replace with your actual DB path
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BookingHistory")  # Fetch all records from the BookingHistory table
    rows = cursor.fetchall()

    # Insert data into the Booking Treeview
    for row in rows:
        booking_tree.insert("", tk.END, values=row)

    conn.close()

def display_pending_bookings():
    admin_frame.pack_forget()  # Hide admin panel
    pending_bookings_frame.pack(fill=tk.BOTH, expand=True)  # Show the pending bookings frame

    # Clear previous entries from the Treeview
    for row in pending_bookings_tree.get_children():
        pending_bookings_tree.delete(row)

    conn = sqlite3.connect("Carmala.db")  # Use your actual DB path
    cursor = conn.cursor()
    cursor.execute("SELECT BookingID, UserID, CarID, PickupDate, DropoffDate, BookingStatus FROM Booking WHERE BookingStatus = 'Pending'")  # Adjust the query if needed
    rows = cursor.fetchall()

    # Insert data into the Pending Bookings Treeview
    for row in rows:
        pending_bookings_tree.insert("", tk.END, values=row)

    conn.close()
# --- MAIN WINDOW SETUP --- #
root = tk.Tk()
root.title("Login Page")
root.geometry('1280x780')

# Main frame for layout
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# --- LOGIN PAGE --- #
login_frame = tk.Frame(main_frame, bg='#F1F1F1')
login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Right side image (during login)
right_frame = tk.Frame(main_frame, bg='#F1F1F1', width=400)
right_frame.pack(fill=tk.Y, side=tk.RIGHT)
image_path = r"C:\Users\User\Downloads\WhatsApp Image 2024-09-24 at 23.17.29_16a30ce5.jpg"  # Add your path
image = Image.open(image_path)
image = ImageTk.PhotoImage(image)
image_label = tk.Label(right_frame, image=image)
image_label.pack(fill=tk.BOTH, expand=True)

# Login form
label_title = tk.Label(login_frame, text="Login", font=("Poppins", 24, "bold"), bg='#F1F1F1')
label_title.pack(pady=20)
label_username = tk.Label(login_frame, text="Username:", bg='#F1F1F1')
label_username.pack()
entry_username = tk.Entry(login_frame)
entry_username.pack(pady=5)

label_password = tk.Label(login_frame, text="Password:", bg='#F1F1F1')
label_password.pack()
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack(pady=5)

button_login = tk.Button(login_frame, text="Log in", font="Poppins", command=login, bg="#1572D3")
button_login.pack(pady=20)
# Edit car button in the Car Availability frame (adjust size)
# Edit car button in the Car Availability frame (adjust size and color)

def approve_booking():
    selected_item = pending_bookings_tree.selection()  # Get the selected item
    if selected_item:
        booking_id = pending_bookings_tree.item(selected_item)["values"][0]  # Get the BookingID of the selected row

        try:
            # Connect to the database
            conn = sqlite3.connect("Carmala.db")
            cursor = conn.cursor()

            # Update the BookingStatus in the Booking table to 'Approved'
            cursor.execute("UPDATE Booking SET BookingStatus = 'Approved' WHERE BookingID = ?", (booking_id,))
            conn.commit()

            # Refresh the pending bookings list
            display_pending_bookings()
            messagebox.showinfo("Success", "Booking status updated to 'Approved' successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Please select a booking to approve.")

def reject_booking():
    selected_item = pending_bookings_tree.selection()  # Get selected item
    if selected_item:
        booking_id = pending_bookings_tree.item(selected_item)["values"][0]  # Get BookingID of selected row

        # Connect to the database
        conn = sqlite3.connect("Carmala.db")  # Use your actual DB path
        cursor = conn.cursor()

        # Fetch the booking details from the Booking table
        cursor.execute("SELECT * FROM Booking WHERE BookingID = ?", (booking_id,))
        booking = cursor.fetchone()

        if booking:
            # Insert the booking details into BookingHistory
            cursor.execute("""
                INSERT INTO BookingHistory (HistoryID, BookingID, PickupDate, DropoffDate)
                VALUES (?, ?, ?, ?)
            """, (None, booking[0], booking[3], booking[4]))  # Adjust indices as per your Booking table structure

            # Delete the booking from the Booking table
            cursor.execute("DELETE FROM Booking WHERE BookingID = ?", (booking_id,))
            conn.commit()  # Commit the changes
            messagebox.showinfo("Success", "Booking rejected successfully!")
        else:
            messagebox.showerror("Error", "Booking not found.")

        conn.close()

        # Refresh the pending bookings list
        display_pending_bookings()
    else:
        messagebox.showerror("Error", "Please select a booking to reject.")

# --- ADMIN PANEL --- #
admin_frame = tk.Frame(main_frame, bg='#F1F1F1')

label_admin_welcome = tk.Label(admin_frame, text="Welcome, Admin!", font=("Poppins", 24, "bold"), bg='#F1F1F1')
label_admin_welcome.pack(pady=20)

admin_image_label = tk.Label(admin_frame)
admin_image_label.pack(fill=tk.BOTH, expand=True)

# Admin panel buttons
button_statistics = tk.Button(admin_frame, text="Booking History", font="Poppins", command=display_booking_history)
button_pending_bookings = tk.Button(admin_frame, text="Pending Bookings", font="Poppins", command=display_pending_bookings)
button_feedback = tk.Button(admin_frame, text="Customer Feedback", font="Poppins", command=lambda: print("Feedback"))
button_manage_cars = tk.Button(admin_frame, text="Show Cars", font="Poppins", command=display_car_availability)
button_agencies = tk.Button(admin_frame, text="Agencies", font="Poppins", command=display_agencies_frame)
button_settings = tk.Button(admin_frame, text="Settings", font="Poppins", command=lambda: print("Settings"))

logout_button = tk.Button(admin_frame, text="Logout", command=logout)
logout_button.place(x=65, y=680, width=180, height=40)

# --- CAR AVAILABILITY PAGE --- #
car_availability_frame = tk.Frame(main_frame, bg='#F1F1F1')
back_button = tk.Button(car_availability_frame, text="Back", command=lambda: [car_availability_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", font="Poppins")
back_button.pack(pady=10)
add_car_button = tk.Button(car_availability_frame, text="Add Car", command=open_add_car_form, bg="#1572D3", font="Poppins")
add_car_button.pack(pady=10)

# Edit car button in the Car Availability frame (adjust size and color)
button_edit_car = tk.Button(car_availability_frame,text="Edit Car",font=("Poppins", 14),bg="green", fg="white",command=lambda: open_edit_car_form())
button_edit_car.pack(pady=10)


# Separate Treeview for car availability
car_columns = ("CarID", "CarName", "CarLocation", "CarCapacity","CarFueltype","CarTransmission","CarFeatures","CarPrice","CarImage","AdminID")
car_tree = ttk.Treeview(car_availability_frame, columns=car_columns, show="headings")
# Add a delete button in the car_availability_frame
delete_button = tk.Button(car_availability_frame, text="Delete Selected", command=delete_selected_row, bg="#FF6347", font="Poppins")
delete_button.pack(pady=10)

car_tree.heading("CarID", text="Car ID")
car_tree.heading("CarName", text="Car Name")
car_tree.heading("CarLocation", text="Car Location")
car_tree.heading("CarCapacity", text="Car Capacity")
car_tree.heading("CarFueltype", text="Car Fuel Type")
car_tree.heading("CarTransmission", text="Car Transmission")
car_tree.heading("CarFeatures", text="Car Features")
car_tree.heading("CarPrice", text="Car Price")
car_tree.heading("CarImage", text="Car Image")
car_tree.heading("AdminID", text="Admin ID")

car_tree.column("CarID", width=100)
car_tree.column("CarName", width=100)
car_tree.column("CarLocation", width=100)
car_tree.column("CarCapacity", width=100)
car_tree.column("CarFueltype", width=100)
car_tree.column("CarTransmission", width=100)
car_tree.column("CarFeatures", width=100)
car_tree.column("CarPrice", width=100)
car_tree.column("CarImage", width=100)
car_tree.column("AdminID", width=100)

car_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


# --- AGENCIES PAGE --- #
agencies_frame = tk.Frame(main_frame, bg='#F1F1F1')
back_button = tk.Button(agencies_frame, text="Back", command=lambda: [agencies_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", font="Poppins")
back_button.pack(pady=10)
agencies_frame = tk.Frame(main_frame, bg='#F1F1F1')
back_button = tk.Button(agencies_frame, text="Back", command=lambda: [agencies_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", font="Poppins")
back_button.pack(pady=10)

# Delete Button for agencies
delete_agency_button = tk.Button(agencies_frame, text="Delete Selected", command=delete_selected_agency, bg="#FF6347", font="Poppins")
delete_agency_button.pack(pady=10)
# Add Button for agencies
add_agency_button = tk.Button(agencies_frame, text="Add New Agency", command=open_add_agency_form, bg="#32CD32", font="Poppins")
add_agency_button.pack(pady=10)

# Separate Treeview for agencies
agency_tree = ttk.Treeview(agencies_frame, columns=("AdminID", "AdminUsername", "AdminPassword","AdminEmail"), show="headings")
agency_tree.heading("AdminID", text="Admin ID")
agency_tree.heading("AdminUsername", text="Admin Username")
agency_tree.heading("AdminPassword", text="Admin Password")
agency_tree.heading("AdminEmail", text="Admin Email")

agency_tree.column("AdminID", width=100)
agency_tree.column("AdminUsername", width=100)
agency_tree.column("AdminPassword", width=100)
agency_tree.column("AdminEmail", width=100)

agency_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
# --- BOOKING HISTORY PAGE --- #
booking_history_frame = tk.Frame(main_frame, bg='#F1F1F1')
back_button = tk.Button(booking_history_frame, text="Back", command=lambda: [booking_history_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", font="Poppins")
back_button.pack(pady=10)

# Define columns for the Booking History Treeview to match your table structure
booking_columns = ("HistoryID", "BookingID", "PickupDate", "DropoffDate")
booking_tree = ttk.Treeview(booking_history_frame, columns=booking_columns, show="headings")

# Define column headers for the new structure
booking_tree.heading("HistoryID", text="Booking ID")
booking_tree.heading("BookingID", text="Booking ID")
booking_tree.heading("PickupDate", text="Pick-Up Date")
booking_tree.heading("DropoffDate", text="Drop-Off Date")


# Define column widths
booking_tree.column("HistoryID", width=100)
booking_tree.column("BookingID", width=120)
booking_tree.column("PickupDate", width=120)
booking_tree.column("DropoffDate", width=120)


# Pack the treeview into the booking history frame
booking_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


# --- PENDING BOOKINGS PAGE --- #
pending_bookings_frame = tk.Frame(main_frame, bg='#F1F1F1')
back_button = tk.Button(pending_bookings_frame, text="Back", command=lambda: [pending_bookings_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", font="Poppins")
back_button.pack(pady=10)

# Define columns for the Pending Bookings Treeview
pending_bookings_columns = ("BookingID", "UserID", "CarID", "PickupDate", "DropoffDate", "BookingStatus")
pending_bookings_tree = ttk.Treeview(pending_bookings_frame, columns=pending_bookings_columns, show="headings")
pending_bookings_tree.heading("BookingID", text="Booking ID")
pending_bookings_tree.heading("UserID", text="User ID")
pending_bookings_tree.heading("CarID", text="Car ID")
pending_bookings_tree.heading("PickupDate", text="Pickup Date")
pending_bookings_tree.heading("DropoffDate", text="Dropoff Date")
pending_bookings_tree.heading("BookingStatus", text="Booking Status")

# Define column widths
pending_bookings_tree.column("BookingID", width=100)
pending_bookings_tree.column("UserID", width=100)
pending_bookings_tree.column("CarID", width=100)
pending_bookings_tree.column("PickupDate", width=100)
pending_bookings_tree.column("DropoffDate", width=100)
pending_bookings_tree.column("BookingStatus", width=100)

# Pack the Treeview into the pending bookings frame
pending_bookings_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Approve and Reject buttons
approve_button = tk.Button(pending_bookings_frame, text="Approve Booking", command=approve_booking, bg="green", font="Poppins", fg="white")
approve_button.pack(side=tk.LEFT, padx=20, pady=10)

reject_button = tk.Button(pending_bookings_frame, text="Reject Booking", command=reject_booking, bg="red", font="Poppins", fg="white")
reject_button.pack(side=tk.LEFT, padx=20, pady=10)

# Update the "Pending Bookings" button to call this function
button_pending_bookings.config(command=display_pending_bookings)


open_admin_panel()

root.mainloop()
