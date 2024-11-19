import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from matplotlib.patches import Patch
import random
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from AdminSession import get_admin_session, set_admin_session


# Global variable to store the session file path
SESSION_FILE = "AdminSession.json"

def open_admin_page():
    logged_in_admin = get_admin_session()
    if logged_in_admin:
        print(f"Welcome, {logged_in_admin['username']} (Admin ID: {logged_in_admin['admin_id']})")
        # Proceed to the admin page
        admin_panel_setup()
    else:
        messagebox.showerror("Access Denied", "Please log in to access the admin panel.")



# Example function to display admin information
def show_admin_info():
    logged_in_admin = get_admin_session()

    if logged_in_admin:
        print(f"Logged in as: {logged_in_admin['username']}, Admin ID: {logged_in_admin['admin_id']}")
    else:
        print("No admin is currently logged in.")




ADMIN_SESSION_FILE = r"C:\Users\User\admin_session.json"

def set_admin_session(admin_data):
    try:
        print("Writing session data:", admin_data)  # Debugging print
        with open(ADMIN_SESSION_FILE, "w") as file:
            json.dump(admin_data, file)
        print(f"Session data written to {ADMIN_SESSION_FILE}.")
    except Exception as e:
        print(f"Error writing session data: {e}")


# Function to get user session (retrieve from session.json)
def get_user_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as file:
            return json.load(file)
    return None  # If the file does not exist, no user is logged in

# Function to clear user session (delete session.json)
def clear_user_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("Session cleared.")


def open_admin_panel():
    # Hide the login frame and display the admin panel
    login_frame.pack_forget()
    admin_frame.pack(fill=tk.BOTH, expand=True)

    # Remove the right side image (used in login page)
    right_frame.pack_forget()

    # Load and set admin-specific image background
    admin_image_path = r"C:\Users\User\Downloads\Group 4.png"  # Add your path
    admin_image = Image.open(admin_image_path)
    admin_image = admin_image.resize((1280, 780), Image.LANCZOS)
    admin_photo = ImageTk.PhotoImage(admin_image)
    admin_image_label.config(image=admin_photo)
    admin_image_label.image = admin_photo  # Keep reference to avoid garbage collection

    # Position buttons on the admin panel
    place_buttons_on_image()

    # Display the statistics chart on the right side
    display_statistics_chart()
    display_revenue_chart()
    display_car_usage_pie_chart()

def check_session():
    admin_session = get_admin_session()
    print("Session data:", admin_session)
    if admin_session:
        print(f"Logged in as Admin ID {admin_session['admin_id']} ({admin_session['username']})")
    else:
        print("No admin logged in.")

# Function to place buttons in the admin panel
def place_buttons_on_image():
    # Side panel buttons
    button_statistics.place(x=65, y=155, width=180, height=40)
    button_pending_bookings.place(x=65, y=205, width=180, height=40)
    button_feedback.place(x=65, y=255, width=180, height=40)
    button_manage_cars.place(x=65, y=305, width=180, height=40)
    button_agencies.place(x=65, y=355, width=180, height=40)
    button_settings.place(x=65, y=405, width=180, height=40)

# Function to get statistics data
def get_statistics_data():
    try:
        # Connect to the database
        conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")
        cursor = conn.cursor()

        # Query to get the total number of bookings
        cursor.execute("SELECT COUNT(*) FROM Booking")
        total = cursor.fetchone()[0]

        # Query to get the number of approved bookings
        cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus = 'Approved'")
        approved = cursor.fetchone()[0]

        # Query to get the number of rejected bookings
        cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus = 'Rejected'")
        rejected = cursor.fetchone()[0]

        # Close the connection
        conn.close()

        return total, approved, rejected

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching statistics data: {e}")
        return 0, 0, 0

# Function to display statistics chart on the right side of the admin panel
def display_statistics_chart():
    total, approved, rejected = get_statistics_data()

    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # Create a Matplotlib figure for the chart
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)

    # Data for the chart
    labels = ['Total', 'Approved', 'Rejected']
    values = [total, approved, rejected]
    colors = ['#4CAF50', '#2196F3', '#F44336']

    # Create a bar chart
    bars = ax.bar(labels, values, color=colors)

    # Set chart title and labels
    ax.set_title("Booking Statistics")
    ax.set_ylabel("Number of Bookings")

    # Display the value on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    # Create a canvas to display the chart in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=admin_frame)
    canvas.draw()
    canvas.get_tk_widget().place(x=850, y=150, width=400, height=400)


def display_statistics():
    total, approved, rejected = get_statistics_data()

    # Create a frame for statistics
    statistics_frame = tk.Frame(admin_frame, bg="#F1F1F1", bd=2, relief=tk.RAISED)
    statistics_frame.place(x=850, y=150, width=350, height=200)

    # Title label
    title_label = tk.Label(statistics_frame, text="Booking Statistics", font=("Arial", 14, "bold"), bg="#F1F1F1")
    title_label.pack(pady=10)

    # Total bookings label
    total_label = tk.Label(statistics_frame, text=f"Total Bookings: {total}", font=("Arial", 12), bg="#F1F1F1")
    total_label.pack(pady=5)

    # Approved bookings label
    approved_label = tk.Label(statistics_frame, text=f"Approved Bookings: {approved}", font=("Arial", 12), bg="#F1F1F1")
    approved_label.pack(pady=5)

    # Rejected bookings label
    rejected_label = tk.Label(statistics_frame, text=f"Rejected Bookings: {rejected}", font=("Arial", 12), bg="#F1F1F1")
    rejected_label.pack(pady=5)

# Function to get revenue statistics data
def get_revenue_statistics():
    try:
        # Connect to the database
        conn = sqlite3.connect(R"C:\Users\User\Downloads\Carmala\main\Carmala.db")
        cursor = conn.cursor()

        # Query to calculate the total revenue
        cursor.execute("SELECT SUM(amount) FROM PaymentTable")
        total_revenue = cursor.fetchone()[0] or 0  # Default to 0 if no data

        # Query to calculate revenue for specific periods (e.g., monthly)
        cursor.execute("""
            SELECT strftime('%Y-%m', Date) as Month, SUM(amount)
            FROM PaymentTable
            GROUP BY Month
            ORDER BY Month
        """)
        monthly_revenue = cursor.fetchall()

        # Close the connection
        conn.close()

        return total_revenue, monthly_revenue

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching revenue data: {e}")
        return 0, []

# Function to display the revenue statistics chart
def display_revenue_chart():
    total_revenue, monthly_revenue = get_revenue_statistics()

    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # Create a Matplotlib figure for the revenue chart
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)

    # Data for the chart
    months = [row[0] for row in monthly_revenue]
    revenues = [row[1] for row in monthly_revenue]
    colors = ['#FFD700' for _ in months]  # Gold color for revenue bars

    # Create a bar chart for monthly revenue
    bars = ax.bar(months, revenues, color=colors)

    # Set chart title and labels
    ax.set_title("Lifetime Revenue Statistics")
    ax.set_ylabel("Revenue (in $)")
    ax.set_xlabel("Month")

    # Rotate and adjust the size of the x-axis labels (months)
    ax.tick_params(axis='x', rotation=0, labelsize=6)  # Rotate and reduce font size of x-axis labels

    # Display the value on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${int(height):,}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    # Create a canvas to display the chart in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=admin_frame)
    canvas.draw()
    canvas.get_tk_widget().place(x=850, y=150, width=400, height=300)


def display_statistics_chart():
    # Booking statistics chart
    total, approved, rejected = get_statistics_data()

    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # Create a Matplotlib figure for the chart
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)

    # Data for the chart
    labels = ['Total', 'Approved', 'Rejected']
    values = [total, approved, rejected]
    colors = ['#4CAF50', '#2196F3', '#F44336']

    # Create a bar chart
    bars = ax.bar(labels, values, color=colors)

    # Set chart title and labels
    ax.set_title("Booking Statistics")
    ax.set_ylabel("Number of Bookings")

    # Rotate and adjust the size of the x-axis labels (total, approved, rejected)
    ax.tick_params(axis='x', rotation=0, labelsize=6)  # Rotate and reduce font size of x-axis labels

    # Display the value on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    # Create a canvas to display the chart in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=admin_frame)
    canvas.draw()
    canvas.get_tk_widget().place(x=400, y=150, width=400, height=300)





def display_pie_chart(data, labels, title, x, y, width=400, height=300):
    """
    Render a pie chart with a side legend for color-coded car representations.

    :param data: List of values for the pie chart.
    :param labels: List of labels corresponding to the data.
    :param title: Title of the pie chart.
    :param x: X-coordinate for the chart position.
    :param y: Y-coordinate for the chart position.
    :param width: Width of the pie chart area.
    :param height: Height of the pie chart area.
    """
    # Generate distinct colors for the pie chart
    colors = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4CAF50",
        "#2196F3", "#F44336", "#9C27B0", "#00BCD4"
    ]
    while len(colors) < len(labels):
        colors.append("#" + "".join(random.choice("0123456789ABCDEF") for _ in range(6)))

    # Create a Matplotlib figure
    fig = Figure(figsize=(5, 3), dpi=100)  # Increased width for side legend
    ax = fig.add_subplot(111)

    # Create the pie chart with reduced percentage size
    wedges, texts, autotexts = ax.pie(
        data,
        labels=None,               # Labels will be displayed in the legend instead
        autopct='%1.0f%%',         # Show integer percentages
        startangle=90,             # Start pie from 12 o'clock
        colors=colors,
        textprops={'fontsize': 8}  # Reduce font size for percentages
    )

    # Add a title to the chart
    ax.set_title(title, fontsize=14)

    # Position the legend on the right side
    fig.subplots_adjust(left=0.3)  # Adjust layout for side legend
    ax.legend(
        handles=[Patch(facecolor=colors[i], label=labels[i]) for i in range(len(labels))],
        title="Cars",
        loc='center left',
        bbox_to_anchor=(1, 0.5),  # Move legend to the side
        fontsize=8,               # Small font for legend
        title_fontsize=10         # Slightly larger font for legend title
    )

    # Embed the chart in the Tkinter admin panel
    canvas = FigureCanvasTkAgg(fig, master=admin_frame)
    canvas.draw()
    canvas.get_tk_widget().place(x=300, y=500, width=900, height=height)




def get_car_usage_data():
    """
    Fetches car usage data by counting the number of bookings for each car.

    :return: A tuple containing two lists: (labels, data)
    """
    try:
        conn = sqlite3.connect(r"C:\Users\User\Downloads\Carmala\main\Carmala.db")
        cursor = conn.cursor()

        # SQL query to join Booking and CarList tables
        query = """
            SELECT CarList.CarName, COUNT(Booking.CarID) AS UsageCount
            FROM Booking
            INNER JOIN CarList ON Booking.CarID = CarList.CarID
            GROUP BY CarList.CarName
            ORDER BY UsageCount DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()

        # Separate data into labels (Car Names) and values (Usage Count)
        labels = [row[0] for row in result]
        data = [row[1] for row in result]

        return labels, data

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching car usage data: {e}")
        return [], []


        # Separate labels (car names) and data (number of bookings)
        labels = [row[0] for row in results]
        data = [row[1] for row in results]

        return labels, data

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching car usage data: {e}")
        return [], []


def display_car_usage_pie_chart():
    """
    Fetches car usage data and displays it as a pie chart on the admin panel.
    """
    labels, data = get_car_usage_data()
    if labels and data:
        display_pie_chart(
            data=data,
            labels=labels,
            title="Car Usage Distribution",
            x=850,  # Position on the admin panel
            y=470
        )


def display_car_availability():
    admin_session = get_admin_session()
    if not admin_session:
        messagebox.showerror("Error", "You must be logged in as an admin to view cars.")
        return

    admin_id = admin_session["admin_id"]  # Retrieve AdminID from session
    print(f"Admin ID from session: {admin_id}")  # Debugging print

    car_availability_frame.pack(fill=tk.BOTH, expand=True)  # Show the car availability frame
    admin_frame.pack_forget()  # Hide admin panel

    # Clear previous entries
    for row in car_tree.get_children():
        car_tree.delete(row)

    try:
        conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
        cursor = conn.cursor()

        # Query to fetch cars associated with the AdminID
        cursor.execute("""
            SELECT * FROM CarList WHERE AdminID = ?
        """, (admin_id,))
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                car_tree.insert("", tk.END, values=row)
        else:
            print(f"No cars found for AdminID {admin_id}.")  # Debugging

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


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
    if os.path.exists(ADMIN_SESSION_FILE):
        os.remove(ADMIN_SESSION_FILE)
    messagebox.showinfo("Logged Out", "You have successfully logged out.")
    root.destroy()  # Close the application


def add_car(name, location, capacity, fueltype, transmission, features, price, image_url, window):
    admin_session = get_admin_session()
    if not admin_session:
        messagebox.showerror("Error", "You must be logged in as an admin to add cars.")
        return

    admin_id = admin_session["admin_id"]  # Get the AdminID from the session

    try:
        conn = sqlite3.connect("Carmala.db")
        cursor = conn.cursor()

        # Insert new car with AdminID
        cursor.execute("""
            INSERT INTO CarList (CarName, CarLocation, CarCapacity, CarFueltype, CarTransmission, CarFeatures, CarPrice, CarImage, AdminID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, location, capacity, fueltype, transmission, features, price, image_url, admin_id))

        conn.commit()
        window.destroy()  # Close the add car window
        messagebox.showinfo("Success", "Car added successfully!")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

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
    admin_session = get_admin_session()
    if not admin_session:
        messagebox.showerror("Error", "You must be logged in as an admin to view booking history.")
        return

    admin_id = admin_session["admin_id"]  # Retrieve AdminID from session
    booking_history_frame.pack(fill=tk.BOTH, expand=True)  # Show booking history frame
    admin_frame.pack_forget()  # Hide admin panel

    # Clear previous entries
    for row in booking_tree.get_children():
        booking_tree.delete(row)

    try:
        conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
        cursor = conn.cursor()

        # Query to fetch booking history associated with the AdminID
        cursor.execute("""
            SELECT HistoryID, BookingID, PickupDate, DropoffDate
            FROM BookingHistory
            WHERE AdminID = ?
        """, (admin_id,))
        rows = cursor.fetchall()

        # Insert data into the Booking Treeview
        for row in rows:
            booking_tree.insert("", tk.END, values=row)

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")



def display_pending_bookings():
    admin_session = get_admin_session()
    if not admin_session:
        messagebox.showerror("Error", "You must be logged in as an admin to view bookings.")
        return

    admin_id = admin_session["admin_id"]  # Retrieve AdminID from session
    pending_bookings_frame.pack(fill=tk.BOTH, expand=True)  # Show the pending bookings frame
    admin_frame.pack_forget()  # Hide admin panel

    # Clear previous entries
    for row in pending_bookings_tree.get_children():
        pending_bookings_tree.delete(row)

    try:
        conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
        cursor = conn.cursor()

        # Filter bookings where AdminID matches
        cursor.execute("""
            SELECT BookingID, UserID, CarID, PickupDate, DropoffDate, BookingStatus
            FROM Booking
            WHERE BookingStatus = 'Pending' AND AdminID = ?
        """, (admin_id,))
        rows = cursor.fetchall()

        # Insert data into the Pending Bookings Treeview
        for row in rows:
            pending_bookings_tree.insert("", tk.END, values=row)

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


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



def send_email_notification(to_email, subject, message):
    sender_email = "killerpill585@gmail.com"
    sender_password = "oxey jnwo qybz etmg"

    try:
        # Set up the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Add the message body
        msg.attach(MIMEText(message, "plain"))

        # Set up the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

def approve_booking():
    selected_item = pending_bookings_tree.selection()  # Get the selected item
    if selected_item:
        booking_id = pending_bookings_tree.item(selected_item)["values"][0]  # Get the BookingID of the selected row

        try:
            # Connect to the database
            conn = sqlite3.connect("Carmala.db")
            cursor = conn.cursor()

            # Fetch the user email, car name, pickup date, and dropoff date
            cursor.execute("""
                SELECT UA.Email, C.CarName, B.PickupDate, B.DropoffDate
                FROM Booking B
                JOIN UserAccount UA ON B.UserID = UA.UserID
                JOIN CarList C ON B.CarID = C.CarID
                WHERE B.BookingID = ?
            """, (booking_id,))
            result = cursor.fetchone()

            if result:
                user_email, car_name, pickup_date, dropoff_date = result

                # Convert dates to readable format
                pickup_date_formatted = pd.to_datetime(pickup_date).strftime("%d %B %Y (%A)")
                dropoff_date_formatted = pd.to_datetime(dropoff_date).strftime("%d %B %Y (%A)")

                # Update the BookingStatus in the Booking table to 'Approved'
                cursor.execute("UPDATE Booking SET BookingStatus = 'Approved' WHERE BookingID = ?", (booking_id,))
                conn.commit()

                # Create the email content
                subject = "Booking Approved"
                message = f"""
                Dear Valued Customer,

                We are pleased to inform you that your booking has been approved!

                **Booking Details:**
                - Car: {car_name}
                - Pickup Date: {pickup_date_formatted}
                - Dropoff Date: {dropoff_date_formatted}
                - Status: Approved

                Please proceed to make payment. Thank you!

                Best regards,
                Carmala Team
                """

                # Send email notification
                send_email_notification(user_email, subject, message)

                # Refresh the pending bookings list
                display_pending_bookings()
                messagebox.showinfo("Success", "Booking status updated to 'Approved' successfully!")

            else:
                messagebox.showerror("Error", "User email or car details not found.")

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

        try:
            # Connect to the database
            conn = sqlite3.connect("Carmala.db")
            cursor = conn.cursor()

            # Fetch the user email, car name, pickup date, and dropoff date
            cursor.execute("""
                SELECT UA.Email, C.CarName, B.PickupDate, B.DropoffDate
                FROM Booking B
                JOIN UserAccount UA ON B.UserID = UA.UserID
                JOIN CarList C ON B.CarID = C.CarID
                WHERE B.BookingID = ?
            """, (booking_id,))
            result = cursor.fetchone()

            if result:
                user_email, car_name, pickup_date, dropoff_date = result

                # Convert dates to readable format
                pickup_date_formatted = pd.to_datetime(pickup_date).strftime("%d %B %Y (%A)")
                dropoff_date_formatted = pd.to_datetime(dropoff_date).strftime("%d %B %Y (%A)")

                # Insert the booking details into BookingHistory
                cursor.execute("""
                    INSERT INTO BookingHistory (HistoryID, BookingID, PickupDate, DropoffDate)
                    SELECT NULL, BookingID, PickupDate, DropoffDate
                    FROM Booking
                    WHERE BookingID = ?
                """, (booking_id,))

                # Delete the booking from the Booking table
                cursor.execute("DELETE FROM Booking WHERE BookingID = ?", (booking_id,))
                conn.commit()

                # Create the email content
                subject = "Booking Rejected"
                message = f"""
                Dear Valued Customer,

                We regret to inform you that your booking has been rejected.

                **Booking Details:**
                - Car: {car_name}
                - Pickup Date: {pickup_date_formatted}
                - Dropoff Date: {dropoff_date_formatted}
                - Status: Rejected

                If you have any questions or need assistance, please contact our support team.

                Best regards,
                Carmala Team
                """

                # Send email notification
                send_email_notification(user_email, subject, message)

                messagebox.showinfo("Success", "Booking rejected successfully!")

            else:
                messagebox.showerror("Error", "User email or car details not found.")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            conn.close()




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
