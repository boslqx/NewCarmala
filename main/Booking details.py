import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
from datetime import datetime
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
               CarList.CarName, CarList.CarPrice, Booking.BookingStatus, AdminAccount.AdminID
        FROM Booking
        JOIN CarList ON Booking.CarID = CarList.CarID
        JOIN AdminAccount ON CarList.AdminID = AdminAccount.AdminID
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

# Proceed to payment
def proceed_to_payment(treeview):
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror("Error", "Please select at least one booking to proceed to payment.")
        return

    selected_bookings = [treeview.item(item)["values"] for item in selected_items]

    # Debugging: Check the structure of selected_bookings
    print("Selected bookings:", selected_bookings)

    # Check for missing or invalid data in the selected bookings
    for booking in selected_bookings:
        if len(booking) < 6 or not isinstance(booking[5], (int, float, str)):
            messagebox.showerror("Error", f"Invalid data for booking: {booking}")
            return

    booking_window.withdraw()
    open_payment_page(selected_bookings)


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
                               fg="white", command=lambda: proceed_to_payment(treeview))
    proceed_button.pack(pady=10)

    cancel_button = tk.Button(booking_window, text="Cancel Booking", font=("Poppins", 12, 'bold'), bg="#D9534F",
                              fg="white", command=cancel_booking)
    cancel_button.pack(pady=10)

    back_button = tk.Button(booking_window, text="Back to Home", font=("Poppins", 12, 'bold'), bg="#1572D3", fg="white",
                            command=go_to_home)
    back_button.pack(pady=10)

    booking_window.mainloop()

def open_payment_page(selected_bookings):
    global payment_window
    payment_window = tk.Toplevel(booking_window)
    payment_window.title("Checkout")
    payment_window.geometry("1280x780")

    # Debugging: Inspect selected_bookings
    print("Selected bookings in payment page:", selected_bookings)

    # Background image setup
    image_path = r"C:\Users\User\OneDrive\Pictures\Group 3.png"
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((1280, 780), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(payment_window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

    def go_back():
        payment_window.destroy()
        booking_window.deiconify()

    button_back = tk.Button(payment_window, text="Back", font=("Arial", 10), bg="#0a47a3", command=go_back)
    button_back.place(x=900, y=125, width=90, height=40)

    # Calculate total price and handle errors
    try:
        total_price = sum([float(booking[5]) for booking in selected_bookings])
    except ValueError as e:
        print("Error in total price calculation:", e)
        messagebox.showerror("Error", "Invalid price data. Cannot calculate total price.")
        return

    # Debugging: Log total price
    print("Total price:", total_price)

    # Booking Details Frame
    details_frame = tk.Frame(payment_window, bg="#FFFFFF", bd=2, relief=tk.GROOVE)
    details_frame.place(x=280, y=280, width=420, height=280)

    # Generate booking details string
    booking_info = ""
    for booking in selected_bookings:
        try:
            car_name = booking[4]
            car_price = booking[5]
            pickup_date = booking[1]
            dropoff_date = booking[2]

            # Format dates
            pickup_date_formatted = datetime.strptime(pickup_date, "%Y-%m-%d").strftime("%d-%m-%Y")
            dropoff_date_formatted = datetime.strptime(dropoff_date, "%Y-%m-%d").strftime("%d-%m-%Y")

            # Calculate number of days booked
            days_booked = (datetime.strptime(dropoff_date, "%Y-%m-%d") - datetime.strptime(pickup_date, "%Y-%m-%d")).days

            booking_info += (
                f"Car: {car_name}, Price: RM{car_price}\n"
                f"From: {pickup_date_formatted}, To: {dropoff_date_formatted}\n"
                f"Days Booked: {days_booked} days\n\n"
            )
        except Exception as e:
            print(f"Error processing booking details for {booking}: {e}")

    # Display booking details
    booking_details_label = tk.Label(details_frame, text=booking_info, font=("Arial", 12), bg="#FFFFFF",
                                     justify="left", anchor="w")
    booking_details_label.pack(padx=10, pady=10)

    # Display total price
    price_label = tk.Label(payment_window, text=f"Total Price: RM{total_price}", font=("Arial", 14, "bold"), bg="#F1F1F1")
    price_label.place(x=770, y=500)

    # Payment Option Buttons
    button_e_wallet = tk.Button(payment_window, text="E-Wallet", font=("Arial", 14), bg="#0a47a3", fg="white",
                                command=lambda: process_payment("E-Wallet"))
    button_e_wallet.place(x=280, y=600, width=230, height=70)

    button_online_banking = tk.Button(payment_window, text="Online Banking", font=("Arial", 14), bg="#0a47a3",
                                      fg="white", command=lambda: process_payment("Online Banking"))
    button_online_banking.place(x=525, y=600, width=230, height=70)

    button_card = tk.Button(payment_window, text="Credit/Debit Card", font=("Arial", 14), bg="#0a47a3", fg="white",
                            command=lambda: process_payment("Credit/Debit Card"))
    button_card.place(x=770, y=600, width=230, height=70)

    def process_payment(payment_type, card_window=None):
        if not selected_bookings:
            messagebox.showerror("Error", "No bookings selected for payment.")
            return

        # Debugging: Inspect selected_bookings structure
        print("Selected bookings:", selected_bookings)

        # Validate data structure
        for booking in selected_bookings:
            if len(booking) < 8:  # Expecting at least 8 fields
                print(f"Invalid booking data: {booking}")
                messagebox.showerror("Error", "Incomplete booking data. Please check your bookings.")
                return

        if payment_type == "Credit/Debit Card":
            # Create a small pop-up window for credit card details
            card_window = tk.Toplevel(payment_window)
            card_window.title("Enter Card Details")
            card_window.geometry("400x250")
            card_window.resizable(False, False)
            card_window.transient(payment_window)  # Keep the pop-up on top of the payment page
            card_window.grab_set()  # Make the pop-up modal (blocks interaction with the main window)

            # Center the pop-up window on the screen
            x = payment_window.winfo_x() + (payment_window.winfo_width() // 2) - 200
            y = payment_window.winfo_y() + (payment_window.winfo_height() // 2) - 125
            card_window.geometry(f"+{x}+{y}")

            # Card Number
            card_number_label = tk.Label(card_window, text="Card Number:", font=("Arial", 12))
            card_number_label.pack(pady=5)
            card_number_entry = tk.Entry(card_window, font=("Arial", 12), width=30)
            card_number_entry.pack(pady=5)

            # Expiry Date
            expiry_date_label = tk.Label(card_window, text="Expiry Date (MM/YY):", font=("Arial", 12))
            expiry_date_label.pack(pady=5)
            expiry_date_entry = tk.Entry(card_window, font=("Arial", 12), width=15)
            expiry_date_entry.pack(pady=5)

            # CVV
            cvv_label = tk.Label(card_window, text="CVV:", font=("Arial", 12))
            cvv_label.pack(pady=5)
            cvv_entry = tk.Entry(card_window, font=("Arial", 12), width=10, show="*")
            cvv_entry.pack(pady=5)

            # Submit Button
            submit_button = tk.Button(card_window, text="Submit", font=("Arial", 14), bg="#0a47a3", fg="white",
                                      command=lambda: finalize_payment("Credit/Debit Card", card_window))
            submit_button.pack(pady=10)

            return  # Exit the current function to wait for user input on the card window


        elif payment_type == "E-Wallet":
            # Show E-Wallet popup and wait for confirmation
            ewallet_window = tk.Toplevel(payment_window)
            ewallet_window.title("E-Wallet Payment")
            ewallet_window.geometry("400x300")

            tk.Label(ewallet_window, text="Select E-Wallet", font=("Arial", 14)).pack(pady=10)

            ewallet_options = ["Touch 'n Go", "Grab Pay", "Boost"]
            selected_ewallet = tk.StringVar(value=ewallet_options[0])

            ewallet_menu = ttk.Combobox(ewallet_window, textvariable=selected_ewallet, values=ewallet_options,
                                        font=("Arial", 12))
            ewallet_menu.pack(pady=20)

            def confirm_ewallet_payment():
                ewallet_choice = selected_ewallet.get()
                messagebox.showinfo("Payment", f"Proceeding with {ewallet_choice} payment.")
                ewallet_window.destroy()
                finalize_payment(payment_type)

            tk.Button(ewallet_window, text="Confirm Payment", font=("Arial", 12), bg="#0a47a3", fg="white",
                      command=confirm_ewallet_payment).pack(pady=20)
            return

        elif payment_type == "Online Banking":
            # Show Online Banking popup and wait for confirmation
            online_banking_window = tk.Toplevel(payment_window)
            online_banking_window.title("Online Banking")
            online_banking_window.geometry("400x350")

            tk.Label(online_banking_window, text="Select Your Bank", font=("Arial", 14)).pack(pady=10)

            bank_options = ["Maybank", "CIMB", "Public Bank", "RHB", "Hong Leong Bank"]
            selected_bank = tk.StringVar(value=bank_options[0])

            bank_menu = ttk.Combobox(online_banking_window, textvariable=selected_bank, values=bank_options,
                                     font=("Arial", 12))
            bank_menu.pack(pady=20)

            tk.Label(online_banking_window, text="Bank Username:", font=("Arial", 12)).pack(pady=5)
            bank_username_entry = tk.Entry(online_banking_window, font=("Arial", 12))
            bank_username_entry.pack(pady=5)

            tk.Label(online_banking_window, text="Bank Password:", font=("Arial", 12)).pack(pady=5)
            bank_password_entry = tk.Entry(online_banking_window, font=("Arial", 12), show="*")
            bank_password_entry.pack(pady=5)

            def confirm_online_banking_payment():
                bank_choice = selected_bank.get()
                username = bank_username_entry.get()
                password = bank_password_entry.get()

                if not username or not password:
                    messagebox.showerror("Input Error", "Please enter your bank login details.")
                    return

                messagebox.showinfo("Payment", f"Logging into {bank_choice} for payment.")
                online_banking_window.destroy()
                finalize_payment(payment_type)

            tk.Button(online_banking_window, text="Confirm Payment", font=("Arial", 12), bg="#0a47a3", fg="white",
                      command=confirm_online_banking_payment).pack(pady=20)
            return

        finalize_payment(payment_type, card_window)

    def finalize_payment(payment_type, card_window=None):
        try:
            total_price = sum([float(booking[5]) for booking in selected_bookings])
            confirm = messagebox.askyesno("Confirm Payment",
                                          f"Do you want to pay RM{total_price} using {payment_type}?")
            if not confirm:
                return

            # Process payment and update the database
            conn = sqlite3.connect('../Carmala.db')
            cursor = conn.cursor()
            payment_successful = True

            for booking in selected_bookings:
                try:
                    booking_id = booking[0]
                    car_id = booking[6]
                    car_price = booking[5]
                    admin_id = booking[7]

                    payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute('''
                        INSERT INTO PaymentTable (PaymentType, BookingID, CarID, Amount, UserID, Date, AdminID)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (payment_type, booking_id, car_id, car_price, user_id, payment_date, admin_id))

                    cursor.execute('''
                        UPDATE Booking
                        SET BookingStatus = 'Paid'
                        WHERE BookingID = ?
                    ''', (booking_id,))

                except Exception as e:
                    print("Error processing booking:", e)
                    messagebox.showerror("Error", f"Unexpected error: {e}")
                    payment_successful = False

            if payment_successful:
                conn.commit()
                messagebox.showinfo("Success", "Payment completed successfully! A receipt and payment confirmation email will be sent to your inbox.")
                if card_window:
                    card_window.destroy()
            else:
                messagebox.showerror("Payment Error", "Payment failed. No changes were committed.")

            conn.close()

        except Exception as e:
            print("Error during payment process:", e)
            messagebox.showerror("Error", f"An error occurred: {e}")


# Run if user is logged in
if user_id:
    open_booking_details_window()
else:
    print("Cannot open booking details window: No user is logged in.")
