import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import Session

# Get the logged-in user's information
logged_in_user = Session.get_user_session()

if logged_in_user:
    user_id = logged_in_user.get("user_id")
    print(f"Logged in user ID: {user_id}")
else:
    print("No user is logged in.")
    user_id = None  # Set user_id to None if no user is logged in

# Function to change button color on hover
def on_hover(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color


def fetch_booking_details(logged_in_user_id):
    # Connect to the database
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    # Query to fetch BookingID, PickupDate, DropoffDate from Booking table and CarName from CarList table,
    # filtered by the logged-in user's UserID
    query = '''
        SELECT Booking.BookingID, Booking.PickupDate, Booking.DropoffDate, CarList.CarName, Booking.BookingStatus
        FROM Booking
        JOIN CarList ON Booking.CarID = CarList.CarID
        WHERE Booking.UserID = ?
    '''
    cursor.execute(query, (logged_in_user_id,))
    bookings = cursor.fetchall()

    conn.close()
    return bookings


def proceed_to_payment():
    print("Proceeding to Payment...")


def go_to_home():
    process = subprocess.Popen(["python", "Home.py"])
    print("Home opened with process ID:", process.pid)
    booking_window.after(400, booking_window.destroy)


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


def open_booking_details_window():
    global booking_window, treeview
    # Create the main window
    booking_window = tk.Tk()
    booking_window.title("Booking Details")
    booking_window.geometry("900x700")
    booking_window.config(bg="#F1F1F1")

    # Create a frame for the treeview
    frame = tk.Frame(booking_window, bg="#F1F1F1")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Create a treeview to display the booking details
    columns = ('BookingID', 'PickupDate', 'DropoffDate', 'CarName', 'BookingStatus')
    treeview = ttk.Treeview(frame, columns=columns, show='headings', height=10)
    treeview.pack(fill=tk.BOTH, expand=True)

    # Define column headings
    treeview.heading('BookingID', text='Booking ID')
    treeview.heading('PickupDate', text='Pickup Date')
    treeview.heading('DropoffDate', text='Dropoff Date')
    treeview.heading('CarName', text='Car Name')
    treeview.heading('BookingStatus', text='Booking Status')

    # Define column widths
    treeview.column('BookingID', width=100)
    treeview.column('PickupDate', width=150)
    treeview.column('DropoffDate', width=150)
    treeview.column('CarName', width=200)
    treeview.column('BookingStatus', width=200)

    # Fetch booking details from the database for the logged-in user and insert into the treeview
    if user_id:
        bookings = fetch_booking_details(user_id)
        for booking in bookings:
            treeview.insert('', 'end', values=booking)

    # "Proceed to Payment" button
    proceed_button = tk.Button(booking_window, text="Proceed to Payment", font=("Poppins", 12, 'bold'),
                               bg="#1572D3", fg="white", command=proceed_to_payment)
    proceed_button.bind("<Enter>", lambda event: on_hover(proceed_button, "#1058A7"))
    proceed_button.bind("<Leave>", lambda event: on_leave(proceed_button, "#1572D3"))
    proceed_button.pack(pady=10)

    # "Cancel Booking" button
    cancel_button = tk.Button(booking_window, text="Cancel Booking", font=("Poppins", 12, 'bold'),
                              bg="#D9534F", fg="white", command=cancel_booking)
    cancel_button.bind("<Enter>", lambda event: on_hover(cancel_button, "#1058A7"))
    cancel_button.bind("<Leave>", lambda event: on_leave(cancel_button, "#D9534F"))
    cancel_button.pack(pady=10)

    # "Back to Home" button
    back_button = tk.Button(booking_window, text="Back to Home", font=("Poppins", 12, 'bold'),
                            bg="#1572D3", fg="white", command=go_to_home)
    back_button.bind("<Enter>", lambda event: on_hover(back_button, "#1058A7"))
    back_button.bind("<Leave>", lambda event: on_leave(back_button, "#1572D3"))

    back_button.pack(pady=10)

    booking_window.mainloop()


# Run the window if a user is logged in
if user_id:
    open_booking_details_window()
else:
    print("Cannot open booking details window: No user is logged in.")
