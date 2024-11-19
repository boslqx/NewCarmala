import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import Session
from datetime import datetime
from tkinter import ttk, messagebox

# Get logged-in user session
logged_in_user = Session.get_user_session()

if logged_in_user:
    user_id = logged_in_user.get("user_id")
    print(f"Logged in user ID: {user_id}")
else:
    print("No user is logged in.")


def fetch_booking_details():
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    query = '''
        SELECT Booking.BookingID, Booking.PickupDate, Booking.DropoffDate, 
               CarList.CarName, CarList.CarPrice, CarList.CarID, CarList.AdminID
        FROM Booking
        JOIN CarList ON Booking.CarID = CarList.CarID
        WHERE Booking.BookingStatus = 'Approved'
    '''
    cursor.execute(query)
    bookings = cursor.fetchall()

    conn.close()
    return bookings


def open_payment_page(selected_bookings):
    global payment_window
    payment_window = tk.Toplevel(booking_window)
    payment_window.title("Checkout")
    payment_window.geometry("1280x780")

    image_path = r"C:\Users\User\Downloads\Group 3.png"
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

    total_price = sum([booking[4] for booking in selected_bookings])

    # Date formatting function
    def format_date(date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %b %Y")

    # Booking Details Frame
    details_frame = tk.Frame(payment_window, bg="#FFFFFF", bd=2, relief=tk.GROOVE)
    details_frame.place(x=280, y=280, width=420, height=280)

    # Booking Info Text (Formatted Dates and Days Booked)
    booking_info = ""
    for booking in selected_bookings:
        car_name = booking[3]
        car_price = booking[4]
        pickup_date = format_date(booking[1])
        dropoff_date = format_date(booking[2])

        # Calculate the number of days booked
        pickup_date_obj = datetime.strptime(booking[1], "%Y-%m-%d")
        dropoff_date_obj = datetime.strptime(booking[2], "%Y-%m-%d")
        days_booked = (dropoff_date_obj - pickup_date_obj).days

        # Format date to dd-mm-yyyy
        # Function to format date to dd-mm-yyyy
        def format_date(date_str):
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d-%m-%Y")

        # Calculate days booked and create booking info string
        booking_info = "\n\n".join([
            f"Car: {booking[3]}, Price: RM{booking[4]}\n"
            f"From: {format_date(booking[1])}, To: {format_date(booking[2])}\n"
            f"Days Booked: {(datetime.strptime(booking[2], '%Y-%m-%d') - datetime.strptime(booking[1], '%Y-%m-%d')).days} days"
            for booking in selected_bookings
        ])

    booking_details_label = tk.Label(details_frame, text=booking_info, font=("Arial", 12), bg="#FFFFFF",
                                     justify="left", anchor="w")
    booking_details_label.pack(padx=10, pady=10)

    # Total Price Label
    price_label = tk.Label(payment_window, text=f" RM{total_price}", font=("Arial", 14, "bold"), bg="#F1F1F1")
    price_label.place(x=825, y=500)

    def show_card_details_popup():
        global card_number_entry, expiry_date_entry, cvv_entry

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
                                  command=lambda: process_payment("Credit/Debit Card", card_window))
        submit_button.pack(pady=10)

        def show_ewallet_popup():
            ewallet_window = tk.Toplevel(payment_window)
            ewallet_window.title("E-Wallet Payment")
            ewallet_window.geometry("400x300")

            tk.Label(ewallet_window, text="Select E-Wallet", font=("Arial", 14)).pack(pady=10)

            # E-Wallet options
            ewallet_options = ["Touch 'n Go", "Grab Pay", "Boost"]
            selected_ewallet = tk.StringVar(value=ewallet_options[0])

            ewallet_menu = ttk.Combobox(ewallet_window, textvariable=selected_ewallet, values=ewallet_options,
                                        font=("Arial", 12))
            ewallet_menu.pack(pady=20)

            # Confirm E-Wallet Payment
            def confirm_ewallet_payment():
                ewallet_choice = selected_ewallet.get()
                messagebox.showinfo("Payment", f"Proceeding with {ewallet_choice} payment.")
                ewallet_window.destroy()

            tk.Button(ewallet_window, text="Confirm Payment", font=("Arial", 12), bg="#0a47a3", fg="white",
                      command=confirm_ewallet_payment).pack(pady=20)

        # Online Banking Payment Method
        def show_online_banking_popup():
            online_banking_window = tk.Toplevel(payment_window)
            online_banking_window.title("Online Banking")
            online_banking_window.geometry("400x350")

            tk.Label(online_banking_window, text="Select Your Bank", font=("Arial", 14)).pack(pady=10)

            # Bank options
            bank_options = ["Maybank", "CIMB", "Public Bank", "RHB", "Hong Leong Bank"]
            selected_bank = tk.StringVar(value=bank_options[0])

            bank_menu = ttk.Combobox(online_banking_window, textvariable=selected_bank, values=bank_options,
                                     font=("Arial", 12))
            bank_menu.pack(pady=20)

            # Bank login form
            tk.Label(online_banking_window, text="Bank Username:", font=("Arial", 12)).pack(pady=5)
            bank_username_entry = tk.Entry(online_banking_window, font=("Arial", 12))
            bank_username_entry.pack(pady=5)

            tk.Label(online_banking_window, text="Bank Password:", font=("Arial", 12)).pack(pady=5)
            bank_password_entry = tk.Entry(online_banking_window, font=("Arial", 12), show="*")
            bank_password_entry.pack(pady=5)

            # Confirm Online Banking Payment
            def confirm_online_banking_payment():
                bank_choice = selected_bank.get()
                username = bank_username_entry.get()
                password = bank_password_entry.get()

                if not username or not password:
                    messagebox.showerror("Input Error", "Please enter your bank login details.")
                    return

                messagebox.showinfo("Payment", f"Logging into {bank_choice} for payment.")
                online_banking_window.destroy()

            tk.Button(online_banking_window, text="Confirm Payment", font=("Arial", 12), bg="#0a47a3", fg="white",
                      command=confirm_online_banking_payment).pack(pady=20)

        # Modify Payment Option Buttons in Payment Page
        button_e_wallet = tk.Button(payment_window, text="E-Wallet", font=("Arial", 14), bg="#0a47a3", fg="white",
                                    command=show_ewallet_popup)
        button_e_wallet.place(x=280, y=600, width=230, height=70)

        button_online_banking = tk.Button(payment_window, text="Online Banking", font=("Arial", 14), bg="#0a47a3",
                                          fg="white",
                                          command=show_online_banking_popup)
        button_online_banking.place(x=525, y=600, width=230, height=70)

        button_card = tk.Button(payment_window, text="Credit/Debit Card", font=("Arial", 14), bg="#0a47a3", fg="white",
                                command=show_card_details_popup)
        button_card.place(x=770, y=600, width=230, height=70)

    # Payment Option Buttons
    button_e_wallet = tk.Button(payment_window, text="E-Wallet", font=("Arial", 14), bg="#0a47a3", fg="white",
                                command=lambda: process_payment("E-Wallet"))
    button_e_wallet.place(x=280, y=600, width=230, height=70)

    button_online_banking = tk.Button(payment_window, text="Online Banking", font=("Arial", 14), bg="#0a47a3",
                                      fg="white", command=lambda: process_payment("Online Banking"))
    button_online_banking.place(x=525, y=600, width=230, height=70)

    button_card = tk.Button(payment_window, text="Credit/Debit Card", font=("Arial", 14), bg="#0a47a3", fg="white",
                            command=show_card_details_popup)

    button_card.place(x=770, y=600, width=230, height=70)

    def process_payment(payment_type, card_window=None):
        if not selected_bookings:
            messagebox.showerror("Error", "No bookings selected for payment.")
            return

        # Get the card details from the form
        card_number = card_number_entry.get()
        expiry_date = expiry_date_entry.get()
        cvv = cvv_entry.get()

        # Ensure card details are provided
        if not card_number or not expiry_date or not cvv:
            messagebox.showerror("Input Error", "Credit/Debit card details are missing.")
            return

        # Validate card number (basic check)
        if len(card_number) < 16 or len(cvv) < 3:
            messagebox.showerror("Input Error", "Invalid card details provided.")
            return

        # Confirm payment
        try:
            total_price = sum([booking[4] for booking in selected_bookings])
            confirm = messagebox.askyesno("Confirm Payment",
                                          f"Do you want to pay RM{total_price} using {payment_type}?")
            if not confirm:
                return

            # Proceed with payment processing (DB insertions, etc.)
            conn = sqlite3.connect('Carmala.db')
            cursor = conn.cursor()
            payment_successful = True

            for booking in selected_bookings:
                try:
                    booking_id = booking[0]
                    car_id = booking[5]
                    car_price = booking[4]
                    admin_id = booking[6]

                    # Insert payment record into PaymentTable
                    payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute('''
                        INSERT INTO PaymentTable (PaymentType, BookingID, CarID, Amount, UserID, Date, AdminID)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (payment_type, booking_id, car_id, car_price, user_id, payment_date, admin_id))

                    # Update Booking status to 'Pending' for admin approval
                    cursor.execute('''
                        UPDATE Booking
                        SET BookingStatus = 'Pending'
                        WHERE BookingID = ?
                    ''', (booking_id,))

                except Exception as e:
                    messagebox.showerror("Error", f"Unexpected error: {e}")
                    payment_successful = False

            if payment_successful:
                conn.commit()
                messagebox.showinfo("Success", "Payment completed successfully! Booking status updated to 'Pending'.")
                if card_window:
                    card_window.destroy()  # Close the pop-up window
            else:
                messagebox.showerror("Payment Error", "Payment failed. No changes were committed.")

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Payment option buttons
    button_e_wallet = tk.Button(payment_window, text="E-Wallet", font=("Arial", 14), bg="#0a47a3", fg="white",
                                command=lambda: process_payment("E-Wallet"))
    button_e_wallet.place(x=280, y=600, width=230, height=70)

    button_online_banking = tk.Button(payment_window, text="Online Banking", font=("Arial", 14), bg="#0a47a3",
                                      fg="white",
                                      command=lambda: process_payment("Online Banking"))
    button_online_banking.place(x=525, y=600, width=230, height=70)

    button_card = tk.Button(payment_window, text="Credit/Debit Card", font=("Arial", 14), bg="#0a47a3", fg="white",
                            command=show_card_details_form)
    button_card.place(x=770, y=600, width=230, height=70)


# Open booking details window
def open_booking_details_window():
    global booking_window
    booking_window = tk.Tk()
    booking_window.title("Booking Details")
    booking_window.geometry("900x700")
    booking_window.config(bg="#F1F1F1")

    frame = tk.Frame(booking_window, bg="#F1F1F1")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    columns = ('BookingID', 'PickupDate', 'DropoffDate', 'CarName', 'CarPrice')
    treeview = ttk.Treeview(frame, columns=columns, show='headings', height=10)
    treeview.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=150)

    bookings = fetch_booking_details()
    for booking in bookings:
        treeview.insert('', 'end', values=booking)

    proceed_button = tk.Button(booking_window, text="Proceed to Payment", font=("Poppins", 12, 'bold'),
                               bg="#1572D3", fg="white", command=lambda: proceed_to_payment(treeview))
    proceed_button.pack(pady=10)

    back_button = tk.Button(booking_window, text="Back to Home", font=("Poppins", 12, 'bold'),
                            bg="#1572D3", fg="white", command=go_to_home)
    back_button.pack(pady=10)

    booking_window.mainloop()


# Proceed to payment
def proceed_to_payment(treeview):
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror("Error", "Please select at least one booking to proceed to payment.")
        return

    selected_bookings = [treeview.item(item)["values"] for item in selected_items]
    booking_window.withdraw()
    open_payment_page(selected_bookings)


# Go to home function
def go_to_home():
    process = subprocess.Popen(["python", "Home.py"])
    print("Home opened with process ID:", process.pid)
    booking_window.after(300, booking_window.destroy)


# Admin approval logic (to be implemented separately)
def approve_booking(booking_id):
    try:
        conn = sqlite3.connect('Carmala.db')
        cursor = conn.cursor()

        # Fetch the booking details
        cursor.execute('''
            SELECT * FROM Booking
            WHERE BookingID = ?
        ''', (booking_id,))
        booking = cursor.fetchone()

        if booking:
            # Move to BookingHistory
            cursor.execute('''
                INSERT INTO BookingHistory (BookingID, UserID, CarID, PickupDate, DropoffDate, Amount, PaymentType, Date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (booking[0], booking[1], booking[2], booking[3], booking[4], booking[5], booking[6], booking[7]))

            # Delete the booking from Booking table
            cursor.execute('''
                DELETE FROM Booking 
                WHERE BookingID = ?
            ''', (booking_id,))

            conn.commit()
            messagebox.showinfo("Success", "Booking approved and moved to history.")
        else:
            messagebox.showerror("Error", "Booking not found.")

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Run the booking details window
open_booking_details_window()
