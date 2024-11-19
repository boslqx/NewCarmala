import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
from PIL import ImageTk, Image
from tkinter import messagebox
import subprocess
from datetime import datetime
import sqlite3
import customtkinter as ctk
import Session

logged_in_user = Session.get_user_session()

if logged_in_user:
    user_id = logged_in_user.get("user_id")
    print(f"Logged in user ID: {user_id}")
    # Proceed with loading user-specific data or UI
else:
    print("No user is logged in.")
    # Handle the case when no user is logged in




# get information from database about car available for renting
def get_available_cars(location, pickup_date, return_date):
    # Connect to the Carmala database
    conn = sqlite3.connect('Carmala.db')
    cursor = conn.cursor()

    # Format dates to match database format (assuming they are stored as text)
    pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
    return_date = datetime.strptime(return_date, '%Y-%m-%d').date()

    # Query to get cars that are available in the specified location
    # and are not booked during the specified date range
    query = """
            SELECT * FROM CarList
            WHERE LOWER(CarLocation) = LOWER(?)
            AND CarID NOT IN (
                SELECT CarID FROM Booking
                WHERE (PickupDate <= ? AND DropoffDate >= ?)
            )
        """

    cursor.execute(query, (location, return_date, pickup_date))
    available_cars = cursor.fetchall()

    # Close the database connection
    conn.close()
    return available_cars

# Function to open the Car List interface with the selected parameters
def open_car_list(location, pickup_date, return_date):
    # Hide the main window
    root.withdraw()

    # Open the external script using subprocess
    process = subprocess.Popen(["python", "Car list.py", location, pickup_date, return_date])
    print("Car list opened with process ID:", process.pid)

    # Poll for the process's status and restore the main window when it finishes
    def check_process():
        if process.poll() is None:  # Process is still running
            root.after(100, check_process)  # Check again after 100ms
        else:
            print("Car List closed")
            root.deiconify()  # Restore the main window

    check_process()

def search_action():
    location = location_entry.get().strip()  # Trim any leading/trailing spaces
    try:
        # Get the pickup and return dates, ensuring they are datetime objects
        pickup_date = pickup_date_entry.get_date()
        if isinstance(pickup_date, str):
            pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d')

        return_date = return_date_entry.get_date()
        if isinstance(return_date, str):
            return_date = datetime.strptime(return_date, '%Y-%m-%d')

        # Format dates as 'YYYY-MM-DD'
        pickup_date_str = pickup_date.strftime('%Y-%m-%d')
        return_date_str = return_date.strftime('%Y-%m-%d')

        # Simple validation to ensure the fields are not empty
        if not location or not pickup_date_str or not return_date_str:
            messagebox.showwarning("Input Error", "Please fill all the fields.")
        else:
            # Call get_available_cars with the correct arguments
            try:
                # Pass pickup_date_str and return_date_str directly
                available_cars = get_available_cars(location, pickup_date_str, return_date_str)
                if not available_cars:
                    messagebox.showinfo("No Cars Available", f"No cars available in {location} during the selected dates.")
                else:
                    # Proceed to open the Car List window without trying to format dates again
                    open_car_list(location, pickup_date_str, return_date_str)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open car list: {str(e)}")
    except Exception as date_error:
        messagebox.showerror("Date Error", f"Failed to parse dates: {str(date_error)}")




def open_userprofile():
    # Hide the main window
    root.withdraw()

    # Open the external script using subprocess
    process = subprocess.Popen(["python", "User profile.py"])
    print("User Profile opened with process ID:", process.pid)

    # Poll for the process's status and restore the main window when it finishes
    def check_process():
        if process.poll() is None:  # Process is still running
            root.after(100, check_process)  # Check again after 100ms
        else:
            print("User Profile closed")
            root.deiconify()  # Restore the main window

    check_process()

# Function to open the script when the "How it Works" button is clicked
def open_howitworks():
    # Hide the main window
    root.withdraw()

    # Open the external script using subprocess
    process = subprocess.Popen(["python", "How it Works.py"])
    print("How it Works opened with process ID:", process.pid)

    # Poll for the process's status and restore the main window when it finishes
    def check_process():
        if process.poll() is None:  # Process is still running
            root.after(100, check_process)  # Check again after 100ms
        else:
            print("How it Works closed")
            root.deiconify()  # Restore the main window

    check_process()

def open_becomearenter():
    # Hide the main window
    root.withdraw()

    # Open the external script using subprocess
    process = subprocess.Popen(["python", "Become a renter.py"])
    print("Become a renter opened with process ID:", process.pid)

    # Poll for the process's status and restore the main window when it finishes
    def check_process():
        if process.poll() is None:  # Process is still running
            root.after(100, check_process)  # Check again after 100ms
        else:
            print("Become a renter closed")
            root.deiconify()  # Restore the main window

    check_process()

# Function to open the script when the "Become a Renter" button is clicked
def open_bookingdetails():
    process = subprocess.Popen(["python", "Booking details.py"])
    print("Booking details opened with process ID:", process.pid)

# Function to handle logout
def log_out():
    Session.clear_user_session()
    root.destroy()
    subprocess.Popen(["python", "Login.py"])

def submit_rating():
    # Get the selected rating (1 to 5)
    rating = rating_var.get()

    # Get the optional comment (if any)
    comment = comment_entry.get("1.0", tk.END).strip()

    # Retrieve the selected car's ID
    selected_car = car_combobox.get()
    if not selected_car:
        messagebox.showwarning("No Car Selected", "Please select a car before submitting.")
        return

    # Retrieve the logged-in user ID (assuming the session data is available)
    logged_in_user = Session.get_user_session()
    if not logged_in_user:
        messagebox.showwarning("Not Logged In", "Please log in to submit a rating.")
        return

    user_id = logged_in_user.get("user_id")

    # Insert rating data into the database
    if rating > 0:
        try:
            # Connect to the Carmala database
            conn = sqlite3.connect("Carmala.db")
            cursor = conn.cursor()

            # Get the CarID based on the selected CarName
            cursor.execute("""
                SELECT CarID FROM CarList WHERE CarName = ?
            """, (selected_car,))
            car_id = cursor.fetchone()
            if not car_id:
                raise ValueError("Selected car not found in the database.")
            car_id = car_id[0]

            # Insert the rating into the Rating table
            cursor.execute("""
                INSERT INTO Rating (UserID, CarID, Stars, Comment) 
                VALUES (?, ?, ?, ?)
            """, (user_id, car_id, rating, comment))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Notify the user and clear the form
            messagebox.showinfo("Thank You", "Your rating has been submitted!")
            print(f"Rating: {rating} star(s)")
            print(f"Car: {selected_car}")
            print(f"Comment: {comment if comment else 'No comment provided'}")

            # Clear the rating, comment fields, and reset the combobox
            rating_var.set(0)
            comment_entry.delete("1.0", tk.END)
            car_combobox.set('')
            for star in stars:
                star.config(text="☆")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
    else:
        messagebox.showwarning("No Rating", "Please select a rating before submitting.")


def open_rating_window():
    global rating_window, rating_var, comment_entry, stars, car_combobox
    logged_in_user = Session.get_user_session()

    if logged_in_user:
        user_id = logged_in_user.get("user_id")
        print(f"Logged in user ID: {user_id}")
        # Proceed with loading user-specific data or UI
    else:
        print("No user is logged in.")
        # Handle the case when no user is logged in

    # Create a new top-level window for the rating UI
    rating_window = tk.Toplevel(root)
    rating_window.title("Rate Your Experience")
    rating_window.geometry("500x400")

    # Label for the rating window
    rating_label = tk.Label(rating_window, text="Please rate your experience:", font=("Arial", 14))
    rating_label.pack(pady=10)

    # Variable to store the rating (1-5)
    rating_var = tk.IntVar(value=0)

    # Frame for the star rating
    star_frame = tk.Frame(rating_window)
    star_frame.pack(pady=10)

    # Create clickable star labels for rating
    stars = []
    for i in range(1, 6):
        star_label = tk.Label(star_frame, text="☆", font=("Arial", 24), fg="gold")
        star_label.grid(row=0, column=i - 1, padx=5)
        star_label.bind("<Button-1>", lambda e, i=i: select_star(i))
        stars.append(star_label)

    # Dropdown for selecting the car
    car_label = tk.Label(rating_window, text="Select the car you booked:", font=("Arial", 10))
    car_label.pack(pady=5)

    car_combobox = ttk.Combobox(rating_window, state="readonly", width=30)
    car_combobox.pack(pady=5)

    # Fetch car names from BookingHistory and CarList
    try:
        conn = sqlite3.connect("Carmala.db")
        cursor = conn.cursor()

        # Inner join BookingHistory and CarList to get CarName for the logged-in user
        cursor.execute("""
            SELECT CarList.CarName 
            FROM Booking
            INNER JOIN CarList ON Booking.CarID = CarList.CarID
            WHERE Booking.UserID = ? AND Booking.BookingStatus = 'Approved'
        """, (logged_in_user.get("user_id"),))
        car_names = [row[0] for row in cursor.fetchall()]

        conn.close()

        # Populate the combobox
        car_combobox['values'] = car_names
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching car data: {e}")

    # Label and entry box for additional comments
    comment_label = tk.Label(rating_window, text="Leave a comment (optional):", font=("Arial", 10))
    comment_label.pack(pady=10)
    comment_entry = tk.Text(rating_window, height=4, width=30)
    comment_entry.pack(pady=5)

    # Submit button to submit the rating and comment
    submit_button = tk.Button(rating_window, text="Submit", command=submit_rating, bg="#1572D3", fg="white",
                              font=("Poppins", 10, "bold"))
    submit_button.pack(pady=10)


chat_window = None
# Function to handle chat button click
def open_chatbox():
    # Chat window
    global chat_window
    chat_window = ctk.CTkToplevel()
    chat_window.title("Chatbot")
    chat_window.geometry("600x600")

    # Set focus to the chat window
    chat_window.focus_force()

    # Disable main window interaction
    chat_window.grab_set()

    BG_GRAY = "#F1F1F1"
    TEXT_COLOR = "black"
    FONT = ("Poppins", 14)
    FONT_BOLD = ("Helvetica", 13, "bold")

    # Send function for chat responses
    def send():
        user_input = e.get()
        txt.configure(state="normal")
        txt.insert("end", "\nYou -> " + user_input)
        txt.configure(state="disabled")

        user_message = user_input.lower()

        if user_message == "hello":
            txt.configure(state="normal")
            txt.insert("end", "\nBot -> Hello! Welcome to GoCar. How can I assist you today?")
            txt.configure(state="disabled")
        elif user_message in ["hi", "hii", "hiiii"]:
            txt.configure(state="normal")
            txt.insert("end", "\nBot -> Hi there! What can I help you with?")
            txt.configure(state="disabled")
        elif user_message == "emergency":
            txt.configure(state="normal")
            txt.insert(
                "end",
                "\nBot -> If this is an emergency, please contact our roadside assistance at 60 3245 5533."
            )
            txt.configure(state="disabled")
        elif user_message in ["how do i rent a car", "how to rent", "how can i rent a car"]:
            txt.configure(state="normal")
            txt.insert(
                "end",
                "\nBot -> To rent a car, you can browse available vehicles on our app, select your preferred car, and follow the steps to book it."
            )
            txt.configure(state="disabled")
        elif user_message in ["i need help with my booking", "booking help", "booking issue"]:
            txt.configure(state="normal")
            txt.insert(
                "end",
                "\nBot -> I'd be happy to help with your booking. Could you please provide your booking ID or more details?"
            )
            txt.configure(state="disabled")
        elif user_message in ["what do you offer", "what cars do you have", "what kinds of cars are available"]:
            txt.configure(state="normal")
            txt.insert(
                "end",
                "\nBot -> We offer a wide range of cars, from compact cars to SUVs and luxury vehicles. You can check availability in your area on our app."
            )
            txt.configure(state="disabled")
        elif user_message in ["thanks", "thank you", "that's helpful"]:
            txt.configure(state="normal")
            txt.insert("end", "\nBot -> You're welcome! Let me know if there's anything else I can assist you with.")
            txt.configure(state="disabled")
        elif user_message in ["i need to cancel my booking", "cancel my booking", "how to cancel"]:
            txt.configure(state="normal")
            txt.insert(
                "end",
                "\nBot -> To cancel a booking, go to 'My Bookings' in the app and select 'Cancel'. If you need further help, let me know."
            )
            txt.configure(state="disabled")
        elif user_message in ["tell me a joke", "make me laugh", "say something funny"]:
            txt.configure(state="normal")
            txt.insert(
                "end",
                "\nBot -> Why don’t cars play hide and seek? Because good luck hiding something that big!"
            )
            txt.configure(state="disabled")
        elif user_message in ["goodbye", "bye", "see you later"]:
            txt.configure(state="normal")
            txt.insert("end", "\nBot -> Thank you for choosing GoCar! Have a safe journey, and see you next time.")
            txt.configure(state="disabled")
        else:
            txt.configure(state="normal")
            txt.insert(
                "end",
                "\nBot -> I'm here to help with any questions about booking, car availability, or your account. Could you please provide more details?"
            )
            txt.configure(state="disabled")

        e.delete(0, "end")

    # Chat interface setup
    label1 = ctk.CTkLabel(chat_window, text="Chat with Us", font=FONT_BOLD, pady=10)
    label1.pack(pady=10)

    txt = ctk.CTkTextbox(chat_window, width=580, height=400, font=FONT)
    txt.pack(pady=10)
    txt.configure(state="disabled")

    e = ctk.CTkEntry(chat_window, width=460, font=FONT)
    e.pack(side="left", padx=10, pady=10)

    send_button = ctk.CTkButton(chat_window, text="Send", font=FONT_BOLD, command=send)
    send_button.pack(side="right", padx=10, pady=10)
    


# Function to change button color on hover
def on_hover(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color


# Create main application window
root = tk.Tk()
root.title("Car Rental Service")
root.geometry("1200x700")  # Adjust window size to fit the design

# Load and set the background image in the Home tab
background_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-10-17 095826.png"  # Your background image path
bg_image = Image.open(background_image_path)
bg_image = bg_image.resize((1200, 700), Image.LANCZOS)  # Resize to fit the window using LANCZOS filter
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to hold the background and other widgets in the Home tab
canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill='both', expand=True)

# Add the background image to the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# create become a renter button
become_renter_button = tk.Button(root, bg="#1572D3",fg="white", text="Become a Renter", font=("Poppins", 12,"bold"), command=open_becomearenter)
become_renter_button.bind("<Enter>", lambda event: on_hover(become_renter_button, "#1058A7"))
become_renter_button.bind("<Leave>", lambda event: on_leave(become_renter_button, "#1572D3"))
canvas.create_window(300, 40, anchor="nw", window=become_renter_button)

# create how it works button
how_it_works_button = tk.Button(root, bg="#1572D3", fg="white",text="How It Works", font=("Poppins", 12,"bold"), command=open_howitworks)
how_it_works_button.bind("<Enter>", lambda event: on_hover(how_it_works_button, "#1058A7"))
how_it_works_button.bind("<Leave>", lambda event: on_leave(how_it_works_button, "#1572D3"))
canvas.create_window(470, 40, anchor="nw", window=how_it_works_button)

# create Booking details button
bookingdetails_button = tk.Button(root, bg="#1572D3", fg="white",text="Booking Details", font=("Poppins", 12,"bold"), command=open_bookingdetails)
bookingdetails_button.bind("<Enter>", lambda event: on_hover(bookingdetails_button, "#1058A7"))
bookingdetails_button.bind("<Leave>", lambda event: on_leave(bookingdetails_button, "#1572D3"))
canvas.create_window(610, 40, anchor="nw", window=bookingdetails_button)

# create user profile button
userprofile_button = tk.Button(root, bg="#1572D3", fg="white",text="Profile", font=("Poppins", 12,"bold"), command=open_userprofile)
userprofile_button.bind("<Enter>", lambda event: on_hover(userprofile_button, "#1058A7"))
userprofile_button.bind("<Leave>", lambda event: on_leave(userprofile_button, "#1572D3"))
canvas.create_window(770, 40, anchor="nw", window=userprofile_button)

# create log out button
logout_button = tk.Button(root, bg="#1572D3", fg="white",text="Log Out", font=("Poppins", 12,"bold"), command=log_out)
logout_button.bind("<Enter>", lambda event: on_hover(logout_button, "#1058A7"))
logout_button.bind("<Leave>", lambda event: on_leave(logout_button, "#1572D3"))
canvas.create_window(1100, 40, anchor="nw", window=logout_button)

# Load images for buttons
chat_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-11-19 163838.png"
rateus_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-11-19 164055.png"

chat_image = Image.open(chat_image_path)
chat_photo = ImageTk.PhotoImage(chat_image.resize((120, 120)))  # Resize as needed

rateus_image = Image.open(rateus_image_path)
rateus_photo = ImageTk.PhotoImage(rateus_image.resize((180, 110)))  # Resize as needed

# Create Chat with Us button using image
chat_button = tk.Button(
    root,
    image=chat_photo,
    command=open_chatbox,
    bd=0,
    highlightthickness=0
)
canvas.create_window(125, 400, anchor="nw", window=chat_button)

# Create Rate Us! button using image
rateus_button = tk.Button(
    root,
    image=rateus_photo,
    command=open_rating_window,
    bd=0,
    highlightthickness=0
)
canvas.create_window(300, 400, anchor="nw", window=rateus_button)


# Create input fields and labels for Location, Pickup Date, and Return Date at the bottom of the page
location_label = tk.Label(root, text="Location", font=("Helvetica", 12), bg="white")
canvas.create_window(100, 600, anchor="nw", window=location_label)

location_entry = tk.Entry(root, font=("Helvetica", 12), width=20)
canvas.create_window(170, 590, anchor="nw", window=location_entry,width=250, height=40)

pickup_label = tk.Label(root, text="Pickup date", font=("Helvetica", 12), bg="white")
canvas.create_window(430, 600, anchor="nw", window=pickup_label)

# Replace the text entry with a calendar date picker (DateEntry)
pickup_date_entry = DateEntry(root, font=("Helvetica", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(520, 590, anchor="nw", window=pickup_date_entry,width=220, height=40)

return_label = tk.Label(root, text="Return date", font=("Helvetica", 12), bg="white")
canvas.create_window(750, 600, anchor="nw", window=return_label)

# Replace the text entry with a calendar date picker (DateEntry)
return_date_entry = DateEntry(root, font=("Helvetica", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
canvas.create_window(840, 590, anchor="nw", window=return_date_entry,width=220, height=40)

# Create the search button
search_button = ttk.Button(root, text="Search", command=search_action)
canvas.create_window(1070, 600, anchor="nw", window=search_button)


# Start the Tkinter event loop
root.mainloop()