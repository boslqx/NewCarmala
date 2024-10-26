import tkinter as tk
from tkinter import ttk
import sqlite3
import subprocess
import Session

logged_in_user = Session.get_user_session()

if logged_in_user:
    user_id = logged_in_user.get("user_id")
    print(f"Logged in user ID: {user_id}")
    # Proceed with loading user-specific data or UI
else:
    print("No user is logged in.")
    # Handle the case when no user is logged in


def fetch_booking_details():
    # Connect to the database
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    # Query to fetch BookingID, PickupDate, DropoffDate from Booking table and CarName from CarList table
    query = '''
        SELECT Booking.BookingID, Booking.PickupDate, Booking.DropoffDate, CarList.CarName
        FROM Booking
        JOIN CarList ON Booking.CarID = CarList.CarID
    '''
    cursor.execute(query)
    bookings = cursor.fetchall()

    conn.close()
    return bookings

def proceed_to_payment():
    # Dummy function for proceeding to payment
    print("Proceeding to Payment...")

def go_to_home():
    process = subprocess.Popen(["python", "Home.py"])
    print("Become a renter opened with process ID:", process.pid)

    # Delay the close of the current window
    booking_window.after(300, booking_window.destroy)  # Waits 300 milliseconds (1 second) before destroying

def open_booking_details_window():
    global booking_window
    # Create the main window
    booking_window = tk.Tk()
    booking_window.title("Booking Details")
    booking_window.geometry("800x600")
    booking_window.config(bg="#F1F1F1")

    # Create a frame for the treeview
    frame = tk.Frame(booking_window, bg="#F1F1F1")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Create a treeview to display the booking details
    columns = ('BookingID', 'PickupDate', 'DropoffDate', 'CarName')
    treeview = ttk.Treeview(frame, columns=columns, show='headings', height=10)
    treeview.pack(fill=tk.BOTH, expand=True)

    # Define column headings
    treeview.heading('BookingID', text='Booking ID')
    treeview.heading('PickupDate', text='Pickup Date')
    treeview.heading('DropoffDate', text='Dropoff Date')
    treeview.heading('CarName', text='Car Name')

    # Define column widths
    treeview.column('BookingID', width=100)
    treeview.column('PickupDate', width=150)
    treeview.column('DropoffDate', width=150)
    treeview.column('CarName', width=200)

    # Fetch booking details from the database and insert into the treeview
    bookings = fetch_booking_details()
    for booking in bookings:
        treeview.insert('', 'end', values=booking)

    # "Proceed to Payment" button
    proceed_button = tk.Button(booking_window, text="Proceed to Payment", font=("Poppins", 12, 'bold'),
                               bg="#1572D3", fg="white", command=proceed_to_payment)
    proceed_button.pack(pady=10)

    # "Back to Home" button
    back_button = tk.Button(booking_window, text="Back to Home", font=("Poppins", 12, 'bold'),
                            bg="#1572D3", fg="white", command=go_to_home)
    back_button.pack(pady=10)

    booking_window.mainloop()

# Run the window
open_booking_details_window()
