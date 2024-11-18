import customtkinter as ctk
from tkcalendar import DateEntry  # CustomTkinter does not have a DateEntry alternative
from PIL import ImageTk, Image
from tkinter import messagebox
import subprocess
from datetime import datetime
import sqlite3
import Session
logged_in_user = Session.get_user_session()

# Initialize the `customtkinter` appearance
ctk.set_appearance_mode("System")  # Options: "System", "Light", "Dark"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

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
                SELECT CarID FROM BookingHistory
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
    try:
        # Call the Car list.py script with the provided arguments directly
        subprocess.Popen(["python", "Car list.py", location, pickup_date, return_date])
        root.after(400, root.destroy)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Car List: {e}")

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




# Function to open the selected button
def open_userprofile():
    process = subprocess.Popen(["python", "User profile.py"])
    print("User Profile opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(400, root.destroy)  # Waits 300 milliseconds (1 second) before destroying

# Function to open the script when the "How it Works" button is clicked
def open_howitworks():
    process = subprocess.Popen(["python", "How it Works.py"])
    print("How it Works opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(400, root.destroy)  # Waits 300 milliseconds (1 second) before destroying

# Function to open the script when the "Become a Renter" button is clicked
def open_becomearenter():
    process = subprocess.Popen(["python", "Become a renter.py"])
    print("Become a renter opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(400, root.destroy)  # Waits 300 milliseconds (1 second) before destroying

# Function to open the script when the "Become a Renter" button is clicked
def open_bookingdetails():
    process = subprocess.Popen(["python", "Booking details.py"])
    print("Booking details opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(400, root.destroy)  # Waits 300 milliseconds (1 second) before destroying

# Function to handle logout
def log_out():
    Session.clear_user_session()
    root.destroy()
    subprocess.Popen(["python", "Login.py"])

# Rating window function and button
def submit_rating():
    # Get the selected rating (1 to 5)
    rating = rating_var.get()

    # Get the optional comment (if any)
    comment = comment_entry.get("1.0", ctk.END).strip()

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

            # Insert the rating into the Rating table
            cursor.execute("""
                INSERT INTO Rating (UserID, Stars, Comment) 
                VALUES (?, ?, ?)
            """, (user_id, rating, comment))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Notify the user and clear the form
            messagebox.showinfo("Thank You", "Your rating has been submitted!")
            print(f"Rating: {rating} star(s)")
            print(f"Comment: {comment if comment else 'No comment provided'}")

            # Clear the rating and comment fields
            rating_var.set(0)
            comment_entry.delete("1.0", ctk.END)
            for star in stars:
                star.config(text="☆")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("No Rating", "Please select a rating before submitting.")


# Star button click function
def select_star(rating):
    rating_var.set(rating)
    # Update star display based on selected rating
    for i in range(1, 6):
        stars[i - 1].config(text="★" if i <= rating else "☆")


def open_rating_window():
    global rating_window, rating_var, comment_entry, stars
    logged_in_user = Session.get_user_session()

    if logged_in_user:
        user_id = logged_in_user.get("user_id")
        print(f"Logged in user ID: {user_id}")
        # Proceed with loading user-specific data or UI
    else:
        print("No user is logged in.")
        # Handle the case when no user is logged in

    # Create a new top-level window for the rating UI
    rating_window = ctk.CTkToplevel(root)
    rating_window.title("Rate Your Experience")
    rating_window.geometry("500x300")

    # Label for the rating window
    rating_label = ctk.CTkLabel(rating_window, text="Please rate your experience:", font=("Arial", 14))
    rating_label.pack(pady=10)

    # Variable to store the rating (1-5)
    rating_var = ctk.IntVar(value=0)

    # Frame for the star rating
    star_frame = ctk.CTkFrame(rating_window)
    star_frame.pack(pady=10)

    # Create clickable star labels for rating
    stars = []
    for i in range(1, 6):
        star_label = ctk.CTkLabel(star_frame, text="☆", font=("Arial", 24), fg="gold")
        star_label.grid(row=0, column=i - 1, padx=5)
        star_label.bind("<Button-1>", lambda e, i=i: select_star(i))
        stars.append(star_label)

    # Label and entry box for additional comments
    comment_label = ctk.CTkLabel(rating_window, text="Leave a comment (optional):", font=("Arial", 10))
    comment_label.pack(pady=10)
    comment_entry = ctk.CTkTextbox(rating_window, height=4, width=30)
    comment_entry.pack(pady=5)

    # Submit button to submit the rating and comment
    submit_button = ctk.CTkButton(rating_window, text="Submit", command=submit_rating, bg="#1572D3", fg="white",
                              font=("Poppins", 10, "bold"))
    submit_button.pack(pady=10)

# Function to handle chat button click
def open_chatbox():
    # Chat window
    chat_window = ctk.CTkToplevel()
    chat_window.title("Chatbot")

    BG_GRAY = "#F1F1F1"
    BG_COLOR = "#F1F1F1"
    TEXT_COLOR = "black"
    FONT = "Poppins 14"
    FONT_BOLD = "Helvetica 13 bold"

    # Send function for chat responses
    def send():
        user_input = e.get()
        txt.insert(ctk.END, "\nYou -> " + user_input)

        user_message = user_input.lower()

        if user_message == "hello":
            txt.insert(ctk.END, "\nBot -> Hello! Welcome to GoCar. How can I assist you today?")
        elif user_message in ["hi", "hii", "hiiii"]:
            txt.insert(ctk.END, "\nBot -> Hi there! What can I help you with?")
        elif user_message == "emergency":
            txt.insert(ctk.END,
                       "\nBot -> If this is an emergency, please contact our roadside assistance at 60 3245 5533.")
        elif user_message in ["how do i rent a car", "how to rent", "how can i rent a car"]:
            txt.insert(ctk.END,
                       "\nBot -> To rent a car, you can browse available vehicles on our app, select your preferred car, and follow the steps to book it.")
        elif user_message in ["i need help with my booking", "booking help", "booking issue"]:
            txt.insert(ctk.END,
                       "\nBot -> I'd be happy to help with your booking. Could you please provide your booking ID or more details?")
        elif user_message in ["what do you offer", "what cars do you have", "what kinds of cars are available"]:
            txt.insert(ctk.END,
                       "\nBot -> We offer a wide range of cars, from compact cars to SUVs and luxury vehicles. You can check availability in your area on our app.")
        elif user_message in ["thanks", "thank you", "that's helpful"]:
            txt.insert(ctk.END, "\nBot -> You're welcome! Let me know if there's anything else I can assist you with.")
        elif user_message in ["i need to cancel my booking", "cancel my booking", "how to cancel"]:
            txt.insert(ctk.END,
                       "\nBot -> To cancel a booking, go to 'My Bookings' in the app and select 'Cancel'. If you need further help, let me know.")
        elif user_message in ["tell me a joke", "make me laugh", "say something funny"]:
            txt.insert(ctk.END,
                       "\nBot -> Why don’t cars play hide and seek? Because good luck hiding something that big!")
        elif user_message in ["goodbye", "bye", "see you later"]:
            txt.insert(ctk.END, "\nBot -> Thank you for choosing GoCar! Have a safe journey, and see you next time.")
        else:
            txt.insert(ctk.END,
                       "\nBot -> I'm here to help with any questions about booking, car availability, or your account. Could you please provide more details?")

        e.delete(0, ctk.END)

    # Chat interface setup
    label1 = ctk.CTkLabel(chat_window, bg='#1572D3', fg=TEXT_COLOR, text="Chat with Us", font=FONT_BOLD, pady=10, width=20, height=1)
    label1.grid(row=0)

    txt = ctk.CTkTextbox(chat_window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)

    scrollbar = ctk.CTkScrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    e = ctk.CTkEntry(chat_window, bg="#F1F1F1", fg=TEXT_COLOR, font=FONT, width=55)
    e.grid(row=2, column=0)

    send_button = ctk.CTkButton(chat_window, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send)
    send_button.grid(row=2, column=1)

# Function to change button color on hover
def on_hover(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color


# Create main application window
root = ctk.CTk()
root.title("Car Rental Service")
root.geometry("1200x700")  # Adjust window size to fit the design

# Load and set the background image
background_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-10-17 095826.png"  # Your background image path
bg_image = Image.open(background_image_path)
bg_image = bg_image.resize((1200, 700), Image.LANCZOS)  # Resize to fit the window using LANCZOS filter
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to hold the background image
canvas = ctk.CTkCanvas(root, width=1200, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create buttons
become_renter_button = ctk.CTkButton(
    master=root, text="Become a Renter", command=open_becomearenter, font=("Poppins", 12, "bold")
)
canvas.create_window(300, 40, anchor="nw", window=become_renter_button)

how_it_works_button = ctk.CTkButton(
    master=root, text="How It Works", command=open_howitworks, font=("Poppins", 12, "bold")
)
canvas.create_window(470, 40, anchor="nw", window=how_it_works_button)

bookingdetails_button = ctk.CTkButton(
    master=root, text="Booking Details", command=open_bookingdetails, font=("Poppins", 12, "bold")
)
canvas.create_window(610, 40, anchor="nw", window=bookingdetails_button)

userprofile_button = ctk.CTkButton(
    master=root, text="Profile", command=open_userprofile, font=("Poppins", 12, "bold")
)
canvas.create_window(770, 40, anchor="nw", window=userprofile_button)

logout_button = ctk.CTkButton(
    master=root, text="Log Out", command=log_out, font=("Poppins", 12, "bold")
)
canvas.create_window(1100, 40, anchor="nw", window=logout_button)

chat_button = ctk.CTkButton(
    master=root, text="Chat with Us", command=open_chatbox, font=("Poppins", 12, "bold"), width=200, height=50
)
canvas.create_window(100, 400, anchor="nw", window=chat_button)

rateus_button = ctk.CTkButton(
    master=root, text="Rate Us", command=open_rating_window, font=("Poppins", 12, "bold"), width=200, height=50
)
canvas.create_window(300, 400, anchor="nw", window=rateus_button)

# Create input fields
location_label = ctk.CTkLabel(root, text="Location", font=("Helvetica", 12))
canvas.create_window(100, 600, anchor="nw", window=location_label)

location_entry = ctk.CTkEntry(root, font=("Helvetica", 12), width=250)
canvas.create_window(170, 590, anchor="nw", window=location_entry, width=250, height=40)

pickup_label = ctk.CTkLabel(root, text="Pickup date", font=("Helvetica", 12))
canvas.create_window(430, 600, anchor="nw", window=pickup_label)

pickup_date_entry = DateEntry(root, font=("Helvetica", 12), width=18, background="darkblue", foreground="white")
canvas.create_window(520, 590, anchor="nw", window=pickup_date_entry, width=220, height=40)

return_label = ctk.CTkLabel(root, text="Return date", font=("Helvetica", 12))
canvas.create_window(750, 600, anchor="nw", window=return_label)

return_date_entry = DateEntry(root, font=("Helvetica", 12), width=18, background="darkblue", foreground="white")
canvas.create_window(840, 590, anchor="nw", window=return_date_entry, width=220, height=40)

# Create the search button
search_button = ctk.CTkButton(root, text="Search", command=search_action, font=("Helvetica", 12))
canvas.create_window(1070, 600, anchor="nw", window=search_button)

# Start the Tkinter event loop
root.mainloop()