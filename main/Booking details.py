import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import Session

# Get the logged-in user's information
logged_in_user = Session.get_user_session()

if logged_in_user:
    user_id = logged_in_user.get("user_id")
    print(f"Logged in user ID: {user_id}")
else:
    print("No user is logged in.")
    user_id = None  # Set user_id to None if no user is logged in


# Function to fetch booking details
def fetch_booking_details(logged_in_user_id, order_by="BookingDate DESC", status_filter=None):
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    query = '''
        SELECT Booking.BookingID, Booking.PickupDate, Booking.DropoffDate, Booking.BookingDate,
               CarList.CarName, Booking.BookingStatus
        FROM Booking
        JOIN CarList ON Booking.CarID = CarList.CarID
        WHERE Booking.UserID = ?
    '''
    if status_filter:
        query += " AND Booking.BookingStatus = ?"
        cursor.execute(query + f" ORDER BY {order_by}", (logged_in_user_id, status_filter))
    else:
        cursor.execute(query + f" ORDER BY {order_by}", (logged_in_user_id,))

    bookings = cursor.fetchall()
    conn.close()
    return bookings


# Function to fetch car details
def fetch_car_details(car_id):
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()
    query = "SELECT * FROM CarList WHERE CarID = ?"
    cursor.execute(query, (car_id,))
    car_details = cursor.fetchone()
    conn.close()
    return car_details


def show_car_details(booking_id):
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    # Fetch car details from the database
    query = '''
        SELECT CarList.CarName, CarList.CarCapacity, CarList.CarFuelType, 
               CarList.CarTransmission, CarList.CarColour, CarList.CarType, CarList.CarImage
        FROM Booking
        JOIN CarList ON Booking.CarID = CarList.CarID
        WHERE Booking.BookingID = ?
    '''
    cursor.execute(query, (booking_id,))
    car_details = cursor.fetchone()
    conn.close()

    # Debugging: Log the fetched data
    print(f"Car details fetched for Booking ID {booking_id}: {car_details}")

    if car_details:
        try:
            # Unpack the car details
            car_name, car_capacity, car_fuel_type, car_transmission, car_colour, car_type, car_image = car_details

            # Create the details window
            car_window = tk.Toplevel(booking_window)
            car_window.title("Car Details")
            car_window.geometry("500x700")
            car_window.config(bg="#FFFFFF")

            # Card-style layout
            card_frame = tk.Frame(car_window, bg="#F9F9F9", bd=2, relief="solid", padx=20, pady=20)
            card_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

            # Display car image
            if car_image and os.path.exists(car_image):
                from PIL import Image, ImageTk
                image = Image.open(car_image)
                image = image.resize((300, 200))  # No need for Image.ANTIALIAS
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(card_frame, image=photo, bg="#F9F9F9")
                image_label.image = photo  # Keep reference
                image_label.pack(pady=10)
            else:
                tk.Label(card_frame, text="Image not available", font=("Poppins", 12), bg="#F9F9F9").pack(pady=10)

            # Add car details
            tk.Label(card_frame, text=f"Car Name: {car_name}", font=("Poppins", 14, "bold"), bg="#F9F9F9").pack(pady=5)
            tk.Label(card_frame, text=f"Capacity: {car_capacity} persons", font=("Poppins", 12), bg="#F9F9F9").pack(pady=5)
            tk.Label(card_frame, text=f"Fuel Type: {car_fuel_type}", font=("Poppins", 12), bg="#F9F9F9").pack(pady=5)
            tk.Label(card_frame, text=f"Transmission: {car_transmission}", font=("Poppins", 12), bg="#F9F9F9").pack(pady=5)
            tk.Label(card_frame, text=f"Colour: {car_colour}", font=("Poppins", 12), bg="#F9F9F9").pack(pady=5)
            tk.Label(card_frame, text=f"Type: {car_type}", font=("Poppins", 12), bg="#F9F9F9").pack(pady=5)

            # Close button
            close_button = tk.Button(car_window, text="Close", font=("Poppins", 12, "bold"),
                                     bg="#1572D3", fg="white", command=car_window.destroy)
            close_button.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying car details: {e}")
            print(f"Error: {e}")

    else:
        messagebox.showwarning("No Data", "No car details found for this booking.")





# Function to filter booking details
def apply_filter():
    order_by = filter_date_var.get()
    status_filter = filter_status_var.get()
    status_filter = None if status_filter == "All" else status_filter
    bookings = fetch_booking_details(user_id, order_by, status_filter)

    # Clear the treeview and repopulate
    for item in treeview.get_children():
        treeview.delete(item)
    for booking in bookings:
        treeview.insert('', 'end', values=booking)


# Proceed to Payment
def proceed_to_payment():
    print("Proceeding to Payment...")


def cancel_booking():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a booking to cancel.")
        return

    booking_id = treeview.item(selected_item[0])['values'][0]

    def submit_cancellation():
        reason = reason_var.get()
        other_reason = other_reason_entry.get().strip() if reason == "Other" else None

        # Connect to the database to delete the selected booking
        conn = sqlite3.connect('Carmala.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Booking WHERE BookingID = ?", (booking_id,))
        conn.commit()
        conn.close()

        treeview.delete(selected_item)
        cancellation_window.destroy()
        messagebox.showinfo("Cancelled", "Booking cancelled successfully.")

    # Create a new window for selecting cancellation reason
    cancellation_window = tk.Toplevel(booking_window)
    cancellation_window.title("Cancel Booking")
    cancellation_window.geometry("400x300")

    tk.Label(cancellation_window, text="Select Reason for Cancellation:", font=("Poppins", 12)).pack(pady=10)

    # Dropdown for reasons
    reason_var = tk.StringVar()
    reasons = ["Change of Plans", "Found a Better Deal", "Need Different Car", "Other"]
    reason_menu = ttk.Combobox(cancellation_window, textvariable=reason_var, values=reasons, state="readonly")
    reason_menu.pack(pady=10)

    # Entry box for "Other" reason
    other_reason_entry = tk.Entry(cancellation_window, font=("Poppins", 10))
    other_reason_entry.pack(pady=10)

    # Update entry box visibility based on reason selection
    def on_reason_change(event):
        if reason_var.get() == "Other":
            other_reason_entry.config(state="normal")
        else:
            other_reason_entry.delete(0, tk.END)
            other_reason_entry.config(state="disabled")

    reason_menu.bind("<<ComboboxSelected>>", on_reason_change)
    other_reason_entry.config(state="disabled")

    submit_button = tk.Button(cancellation_window, text="Submit", command=submit_cancellation, bg="#1572D3", fg="white",
                              font=("Poppins", 12, 'bold'))
    submit_button.pack(pady=20)


# Back to Home
def go_to_home():
    booking_window.destroy()


# Main Function
def open_booking_details_window():
    global booking_window, treeview, filter_date_var, filter_status_var
    booking_window = tk.Tk()
    booking_window.title("Booking Details")
    booking_window.geometry("1000x700")
    booking_window.config(bg="#F1F1F1")

    frame = tk.Frame(booking_window, bg="#F1F1F1")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    columns = ('BookingID', 'PickupDate', 'DropoffDate', 'BookingDate', 'CarName', 'BookingStatus')
    treeview = ttk.Treeview(frame, columns=columns, show='headings', height=10)
    treeview.pack(fill=tk.BOTH, expand=True)

    treeview.heading('BookingID', text='Booking ID')
    treeview.heading('PickupDate', text='Pickup Date')
    treeview.heading('DropoffDate', text='Dropoff Date')
    treeview.heading('BookingDate', text='Booking Date')
    treeview.heading('CarName', text='Car Name')
    treeview.heading('BookingStatus', text='Booking Status')

    treeview.column('BookingID', width=100)
    treeview.column('PickupDate', width=150)
    treeview.column('DropoffDate', width=150)
    treeview.column('BookingDate', width=150)
    treeview.column('CarName', width=200)
    treeview.column('BookingStatus', width=200)

    # Add a note below the treeview
    note_label = tk.Label(frame, text="*Double-click on a booking to view car details*",
                          font=("Poppins", 10, "italic"), fg="gray", bg="#F1F1F1")
    note_label.pack(pady=5)

    bookings = fetch_booking_details(user_id)
    for booking in bookings:
        treeview.insert('', 'end', values=booking)

    def on_treeview_select(event):
        selected_item = treeview.selection()
        if selected_item:
            booking_id = treeview.item(selected_item[0])['values'][0]
            show_car_details(booking_id)

    treeview.bind("<Double-1>", on_treeview_select)

    # Filter options
    filter_frame = tk.Frame(booking_window, bg="#F1F1F1")
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Sort by Date:", font=("Poppins", 12), bg="#F1F1F1").pack(side=tk.LEFT, padx=5)
    filter_date_var = tk.StringVar(value="Newest")
    date_menu = ttk.Combobox(filter_frame, textvariable=filter_date_var, values=["Newest", "Oldest"],
                             state="readonly")
    date_menu.pack(side=tk.LEFT, padx=5)

    tk.Label(filter_frame, text="Filter by Status:", font=("Poppins", 12), bg="#F1F1F1").pack(side=tk.LEFT, padx=5)
    filter_status_var = tk.StringVar(value="All")
    status_menu = ttk.Combobox(filter_frame, textvariable=filter_status_var,
                               values=["All", "Approved", "Pending", "Rejected"], state="readonly")
    status_menu.pack(side=tk.LEFT, padx=5)

    apply_button = tk.Button(filter_frame, text="Apply Filter", command=apply_filter, bg="#1572D3", fg="white",
                             font=("Poppins", 12, 'bold'))
    apply_button.pack(side=tk.LEFT, padx=10)

    # Buttons
    proceed_button = tk.Button(booking_window, text="Proceed to Payment", font=("Poppins", 12, 'bold'), bg="#1572D3",
                               fg="white", command=proceed_to_payment)
    proceed_button.pack(pady=10)

    cancel_button = tk.Button(booking_window, text="Cancel Booking", font=("Poppins", 12, 'bold'), bg="#D9534F",
                              fg="white", command=cancel_booking)
    cancel_button.pack(pady=10)

    back_button = tk.Button(booking_window, text="Back to Home", font=("Poppins", 12, 'bold'), bg="#1572D3", fg="white",
                            command=go_to_home)
    back_button.pack(pady=10)

    booking_window.mainloop()


# Run if user is logged in
if user_id:
    open_booking_details_window()
else:
    print("Cannot open booking details window: No user is logged in.")
