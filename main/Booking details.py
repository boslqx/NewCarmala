import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
from datetime import datetime
import Session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Get the logged-in user's information
logged_in_user = Session.get_user_session()

if logged_in_user:
    user_id = logged_in_user.get("user_id")
    print(f"Logged in user ID: {user_id}")
else:
    print("No user is logged in.")
    user_id = None  # Set user_id to None if no user is logged in


def fetch_booking_details(logged_in_user_id, order_by="BookingDate DESC", status_filter=None):
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    query = '''
        SELECT Booking.BookingID, Booking.PickupDate, Booking.DropoffDate, Booking.BookingDate,
       CarList.CarName, CarList.CarPrice, Booking.BookingStatus, CarList.CarID, 
       AdminAccount.AdminID, UserAccount.Email
        FROM Booking
        JOIN CarList ON Booking.CarID = CarList.CarID
        JOIN AdminAccount ON CarList.AdminID = AdminAccount.AdminID
        JOIN UserAccount ON Booking.UserID = UserAccount.UserID
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

def proceed_to_payment(treeview):
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror("Error", "Please select at least one booking to proceed to payment.")
        return

    selected_bookings = [treeview.item(item)["values"] for item in selected_items]

    # Debugging: Log selected bookings
    print("Selected bookings:", selected_bookings)

    total_price = 0  # Initialize total price

    # Calculate total price based on the number of days booked
    for booking in selected_bookings:
        car_price = float(booking[5])  # CarPrice is at index 5
        pickup_date = datetime.strptime(booking[1], "%Y-%m-%d")  # PickupDate is at index 1
        dropoff_date = datetime.strptime(booking[2], "%Y-%m-%d")  # DropoffDate is at index 2

        # Calculate number of days booked (inclusive)
        days_booked = (dropoff_date - pickup_date).days + 1
        print(f"Booking ID {booking[0]}: Pickup Date = {pickup_date}, Dropoff Date = {dropoff_date}, Days Booked = {days_booked}")

        if days_booked < 0:
            messagebox.showerror("Error", f"Invalid booking dates for booking ID: {booking[0]}")
            return

        # Calculate total price for this booking
        booking_price = car_price * days_booked
        print(f"Booking ID {booking[0]}: Car Price = RM{car_price}, Days Booked = {days_booked}, Total = RM{booking_price}")
        total_price += booking_price

    # Debugging: Log total price
    print(f"Total price for all bookings: RM{total_price}")
    # Pass total price to the payment page
    booking_window.withdraw()
    open_payment_page(selected_bookings, total_price)



# Main Function
def open_booking_details_window():
    global booking_window, treeview, filter_date_var, filter_status_var
    booking_window = tk.Tk()
    booking_window.title("Booking Details")
    booking_window.geometry("1280x700")
    booking_window.config(bg="#F1F1F1")

    frame = tk.Frame(booking_window, bg="#F1F1F1")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    columns = ('BookingID', 'PickupDate', 'DropoffDate', 'BookingDate', 'CarName', 'CarPrice', 'BookingStatus')
    treeview = ttk.Treeview(frame, columns=columns, show='headings', height=10)
    treeview.pack(fill=tk.BOTH, expand=True)

    treeview.heading('BookingID', text='Booking ID')
    treeview.heading('PickupDate', text='Pickup Date')
    treeview.heading('DropoffDate', text='Dropoff Date')
    treeview.heading('BookingDate', text='Booking Date')
    treeview.heading('CarName', text='Car Name')
    treeview.heading('CarPrice', text='Car Price (RM)')
    treeview.heading('BookingStatus', text='Booking Status')

    treeview.column('BookingID', width=100)
    treeview.column('PickupDate', width=150)
    treeview.column('DropoffDate', width=150)
    treeview.column('BookingDate', width=150)
    treeview.column('CarName', width=200)
    treeview.column('CarPrice', width=120)
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

def open_payment_page(selected_bookings, total_price):
    global payment_window
    payment_window = tk.Toplevel(booking_window)
    payment_window.title("Checkout")
    payment_window.geometry("910x760")

    # Debugging: Inspect selected_bookings
    print("Selected bookings in payment page:", selected_bookings)

    # Background image setup
    image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-11-20 224726.png"
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((910, 760), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(payment_window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

    def go_back():
        payment_window.destroy()
        booking_window.deiconify()

    button_back = tk.Button(payment_window, text="Back to Booking", font=("Arial", 10,"bold"), bg="#1572D3",fg = "white", command=go_back)
    button_back.place(x=690, y=115, width=160, height=30)

    # Booking Details Frame
    details_frame = tk.Frame(payment_window, bg="#FFFFFF", bd=2, relief=tk.GROOVE)
    details_frame.place(x=103, y=275, width=455, height=289)

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
                f"Days Booked: {1 + days_booked} days\n\n"
            )
        except Exception as e:
            print(f"Error processing booking details for {booking}: {e}")

    # Display booking details
    booking_details_label = tk.Label(details_frame, text=booking_info, font=("Arial", 12), bg="#FFFFFF",
                                     justify="left", anchor="w")
    booking_details_label.pack(padx=10, pady=10)

    # Debugging: Inspect total price and selected bookings
    print(f"Total price passed to payment page: RM{total_price}")
    print("Selected bookings passed to payment page:", selected_bookings)

    # price label
    price_label = tk.Label(payment_window, text=f"Total Price: RM{total_price}", font=("Arial", 14, "bold"),bg="#FEFEFE")
    price_label.place(x=593, y=500)

    # Payment Option Buttons
    button_e_wallet = tk.Button(payment_window, text="E-Wallet", font=("Arial", 14), bg="#0F4EDE", fg="white",
                                command=lambda: process_payment("E-Wallet"))
    button_e_wallet.place(x=120, y=590, width=230, height=70)

    button_online_banking = tk.Button(payment_window, text="Online Banking", font=("Arial", 14), bg="#0BDFDF",
                                      fg="white", command=lambda: process_payment("Online Banking"))
    button_online_banking.place(x=335, y=590, width=230, height=70)

    button_card = tk.Button(payment_window, text="Credit/Debit Card", font=("Arial", 14), bg="#0CBDA8", fg="white",
                            command=lambda: process_payment("Credit/Debit Card"))
    button_card.place(x=560, y=590, width=230, height=70)

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

    def generate_receipt_pdf(booking, total_price, file_path="receipt.pdf"):
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Add details to the PDF
        c.setFont("Helvetica", 12)
        c.drawString(30, height - 40, f"Receipt for Booking {booking[0]}")
        c.drawString(30, height - 60, f"Car: {booking[4]}")  # Car Name
        c.drawString(30, height - 80, f"Pickup Date: {booking[1]}")
        c.drawString(30, height - 100, f"Dropoff Date: {booking[2]}")
        c.drawString(30, height - 120, f"Total Price: RM {total_price}")
        c.drawString(30, height - 140, f"Username: {booking[3]}")  # Assuming booking[3] is the username
        c.drawString(30, height - 160, f"Email: {booking[4]}")  # Assuming booking[4] is the email

        # Footer with Admin contact info
        admin_email = "admin@example.com"  # Replace with actual admin email
        c.drawString(30, 30, f"Contact Admin: {admin_email}")

        c.save()

    def send_email(user_email, booking, total_price, receipt_file_path="receipt.pdf"):
        admin_email = "killerpill585@gmail.com"  # Replace with actual admin email
        admin_password = "oxey jnwo qybz etmg"  # Replace with actual admin email password

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = admin_email
        msg['To'] = user_email
        msg['Subject'] = "Booking Confirmation and Receipt"

        # Body of the email
        body = f"""
        Dear {booking[3]}, 

        Your booking for the car {booking[4]} has been successfully processed.

        Booking Details:
        Pickup Date: {booking[1]}
        Dropoff Date: {booking[2]}
        Total Price: RM {total_price}

        If you have any questions, feel free to contact the admin at {admin_email}.
        """

        msg.attach(MIMEText(body, 'plain'))

        # Attach the receipt PDF
        with open(receipt_file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{receipt_file_path}"')
            msg.attach(part)

        print(f"Admin Email: {admin_email}")
        print(f"Recipient Email: {user_email}")
        print(f"Booking Details: {booking}")
        print(f"Receipt File Path: {receipt_file_path}")

        # Send the email via SMTP
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(admin_email, admin_password)
            text = msg.as_string()
            server.sendmail(admin_email, user_email, text)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

    def is_valid_email(email):
        import re
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    def finalize_payment(payment_type, card_window=None):
        try:
            total_price = sum([float(booking[5]) for booking in selected_bookings])
            confirm = messagebox.askyesno("Confirm Payment",
                                          f"Do you want to pay RM{total_price} using {payment_type}?")
            if not confirm:
                return

            conn = sqlite3.connect('Carmala.db')  # Adjust path if necessary
            cursor = conn.cursor()
            payment_successful = True

            # Process each selected booking
            for booking in selected_bookings:
                try:
                    # Assuming email is at index 9 after updating your database query
                    user_email = booking[9]

                    # Validate the email address
                    if not is_valid_email(user_email):
                        print(f"Invalid email detected: {user_email}")
                        messagebox.showerror("Error", f"Invalid email address: {user_email}")
                        continue  # Skip processing this booking

                    # Proceed with email and payment processing
                    send_email(user_email, booking, total_price)

                    # Other payment processing logic here...

                except Exception as e:
                    print(f"Error processing booking {booking[0]}: {e}")
                    messagebox.showerror("Error", f"Unexpected error: {e}")
                    payment_successful = False

            if payment_successful:
                conn.commit()
                messagebox.showinfo("Success", "Payment completed successfully! A receipt has been sent to your email.")
                if card_window:
                    card_window.destroy()  # Close the payment window

                # Return to the Booking Details window
                booking_window.deiconify()  # Assuming you have this window referenced

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
