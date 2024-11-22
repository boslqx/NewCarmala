import tkinter as tk
from tkinter import messagebox, filedialog
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
import Session
from tkinter import Toplevel, Label, Button
import io
from tkinter import Text
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


ADMIN_SESSION_FILE = "AdminSession.json"
# Function to retrieve admin session and show admin details
def get_logged_in_admin():
    admin_session = Session.get_admin_session()
    if admin_session:
        admin_id = admin_session["admin_id"]
        admin_username = admin_session["username"]
        print(f"Admin ID: {admin_id}, Username: {admin_username}")  # Debugging print
        return admin_id, admin_username
    print("No admin is logged in.")
    return None, None  # If no session exists

def get_admin_session():
    """Retrieve the admin session data from the JSON file."""
    if os.path.exists(ADMIN_SESSION_FILE):
        try:
            with open(ADMIN_SESSION_FILE, "r") as file:
                session_data = json.load(file)
                print("[DEBUG] Admin session loaded:", session_data)
                return session_data
        except json.JSONDecodeError:
            print("[ERROR] Session file is corrupted.")
    print("[DEBUG] No session file found.")
    return None
# Function to clear the admin session
def clear_admin_session():
    """Delete the admin session file."""
    if os.path.exists(ADMIN_SESSION_FILE):
        os.remove(ADMIN_SESSION_FILE)
        print("[DEBUG] Admin session cleared.")

def open_admin_page(admin_data):
    global CURRENT_ADMIN
    CURRENT_ADMIN = admin_data  # Store admin data globally
    print(f"Admin page opened for: {CURRENT_ADMIN['username']} (Admin ID: {CURRENT_ADMIN['admin_id']})")
    # Proceed to display the admin panel
    open_admin_panel()
logged_in_admin = get_admin_session()

if logged_in_admin:
    admin_id = logged_in_admin.get("admin_id")
    print(f"[DEBUG] Logged in Admin ID: {admin_id}")
else:
    messagebox.showerror("Access Denied", "No admin session found. Please log in again.")
    os.system("python Login.py")  # Redirect to login page
    exit()

def show_admin_info():
    if logged_in_admin:
        print(f"Logged in as: {logged_in_admin['username']}, Admin ID: {logged_in_admin['admin_id']}")
    else:
        print("No admin is currently logged in.")

# Function to change button color on hover
def on_hover(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color

def open_admin_panel():
    # Hide the login frame and display the admin panel
    login_frame.pack_forget()
    admin_frame.pack(fill=tk.BOTH, expand=True)

    # Remove the right side image (used in login page)
    right_frame.pack_forget()

    # Load and set admin-specific image background
    admin_image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-11-21 194312.png"
    admin_image = Image.open(admin_image_path)
    admin_image = admin_image.resize((1200, 700), Image.LANCZOS)
    admin_photo = ImageTk.PhotoImage(admin_image)
    admin_image_label.config(image=admin_photo)
    admin_image_label.image = admin_photo  # Keep reference to avoid garbage collection

    # Position buttons on the admin panel
    place_buttons_on_image()

    # Database connection
    connection = sqlite3.connect("Carmala.db")  # Adjust the database name/path as necessary
    cursor = connection.cursor()

    # Fetch the AdminUsername
    query = "SELECT AdminUsername FROM AdminAccount WHERE AdminID = ?"
    cursor.execute(query, (admin_id,))
    result = cursor.fetchone()

    # Check if a result is found
    if result:
        admin_username = result[0]
        print(f"Welcome, {admin_username}!")  # Or use it in a Tkinter label
    else:
        print("Admin not found!")

    welcome_label = tk.Label(admin_frame, text=f"Welcome, {admin_username}", font=("Poor Richard", 20, "bold"),
                             bg="#FFFFFF", fg="black")
    welcome_label.place(x=210, y=40)

    stats_label = tk.Label(admin_frame, text="Statistic Report", font=("Poppibs", 14, "bold underline"),
                             bg="#FFFFFF", fg="black")
    stats_label.place(x=600, y=90)

    # Display the statistics chart on the right side
    display_statistics_chart()
    display_revenue_chart()
    display_car_usage_pie_chart()

# Function to place buttons in the admin panel
def place_buttons_on_image():
    # Side panel buttons
    button_pending_bookings.place(x=10, y=155, width=180, height=40)

    button_feedback.place(x=10, y=205, width=180, height=40)
    button_manage_cars.place(x=10, y=255, width=180, height=40)
    button_agencies.place(x=10, y=305, width=180, height=40)
    button_manage_users.place(x=10, y=355, width=180, height=40)
    button_print.place(x=10, y=405, width=180, height=40)


def get_statistics_data():
    try:
        # Retrieve the logged-in admin's session data
        admin_session = Session.get_admin_session()
        if not admin_session or "admin_id" not in admin_session:
            messagebox.showerror("Error", "You must be logged in as an admin to view statistics.")
            return 0, 0, 0

        admin_id = admin_session["admin_id"]
        is_superadmin = admin_session.get("SuperAdmin", False)  # Check if the admin is a SuperAdmin

        # Connect to the database
        conn = sqlite3.connect("Carmala.db")
        cursor = conn.cursor()

        # Conditional filtering for SuperAdmin
        if is_superadmin:
            cursor.execute("SELECT COUNT(*) FROM Booking")
        else:
            cursor.execute("SELECT COUNT(*) FROM Booking WHERE AdminID = ?", (admin_id,))
        total = cursor.fetchone()[0]

        if is_superadmin:
            cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus = 'Approved'")
        else:
            cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus = 'Approved' AND AdminID = ?", (admin_id,))
        approved = cursor.fetchone()[0]

        if is_superadmin:
            cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus = 'Rejected'")
        else:
            cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus = 'Rejected' AND AdminID = ?", (admin_id,))
        rejected = cursor.fetchone()[0]

        conn.close()
        return total, approved, rejected

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching statistics data: {e}")
        return 0, 0, 0

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

def get_revenue_statistics():
    try:
        # Retrieve the logged-in admin's session data
        admin_session = Session.get_admin_session()
        if not admin_session or "admin_id" not in admin_session:
            messagebox.showerror("Error", "You must be logged in as an admin to view revenue statistics.")
            return 0, []

        admin_id = admin_session["admin_id"]
        is_superadmin = admin_session.get("SuperAdmin", False)  # Check if the admin is a SuperAdmin

        # Connect to the database
        conn = sqlite3.connect("Carmala.db")
        cursor = conn.cursor()

        # Conditional filtering for SuperAdmin
        if is_superadmin:
            cursor.execute("SELECT SUM(amount) FROM PaymentTable")
        else:
            cursor.execute("SELECT SUM(amount) FROM PaymentTable WHERE AdminID = ?", (admin_id,))
        total_revenue = cursor.fetchone()[0] or 0  # Default to 0 if no data

        if is_superadmin:
            cursor.execute("""
                SELECT strftime('%Y-%m', Date) as Month, SUM(amount)
                FROM PaymentTable
                GROUP BY Month
                ORDER BY Month
            """)
        else:
            cursor.execute("""
                SELECT strftime('%Y-%m', Date) as Month, SUM(amount)
                FROM PaymentTable
                WHERE AdminID = ?
                GROUP BY Month
                ORDER BY Month
            """, (admin_id,))
        monthly_revenue = cursor.fetchall()

        conn.close()
        return total_revenue, monthly_revenue

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching revenue data: {e}")
        return 0, []

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
    canvas.get_tk_widget().place(x=750, y=123, width=400, height=300)


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
    canvas.get_tk_widget().place(x=230, y=123, width=400, height=300)





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
    canvas.get_tk_widget().place(x=200, y=430, width=780, height=height)




def get_car_usage_data():
    try:
        # Retrieve the logged-in admin's session data
        admin_session = Session.get_admin_session()
        if not admin_session or "admin_id" not in admin_session:
            messagebox.showerror("Error", "You must be logged in as an admin to view car usage data.")
            return [], []

        admin_id = admin_session["admin_id"]
        is_superadmin = admin_session.get("SuperAdmin", False)  # Check if the admin is a SuperAdmin

        # Connect to the database
        conn = sqlite3.connect("carmala.db")
        cursor = conn.cursor()

        # Conditional filtering for SuperAdmin
        if is_superadmin:
            query = """
                SELECT CarList.CarName, COUNT(Booking.CarID) AS UsageCount
                FROM Booking
                INNER JOIN CarList ON Booking.CarID = CarList.CarID
                GROUP BY CarList.CarName
                ORDER BY UsageCount DESC
            """
            cursor.execute(query)
        else:
            query = """
                SELECT CarList.CarName, COUNT(Booking.CarID) AS UsageCount
                FROM Booking
                INNER JOIN CarList ON Booking.CarID = CarList.CarID
                WHERE CarList.AdminID = ?
                GROUP BY CarList.CarName
                ORDER BY UsageCount DESC
            """
            cursor.execute(query, (admin_id,))
        result = cursor.fetchall()
        conn.close()

        # Separate data into labels (Car Names) and values (Usage Count)
        labels = [row[0] for row in result]
        data = [row[1] for row in result]

        return labels, data

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching car usage data: {e}")
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
    # Retrieve the logged-in admin's session data
    admin_session = Session.get_admin_session()

    if not admin_session or "admin_id" not in admin_session:
        messagebox.showerror("Error", "You must be logged in as an admin to view car availability.")
        return

    # Debugging output
    print(f"[DEBUG] Admin session loaded in adminpage: {admin_session}")

    # Retrieve Admin ID and SuperAdmin status from session
    admin_id = admin_session["admin_id"]  # Retrieve AdminID from session
    is_superadmin = admin_session.get("SuperAdmin", False)  # Check if the admin is a SuperAdmin
    print(f"[DEBUG] Displaying cars for Admin ID: {admin_id} (SuperAdmin: {is_superadmin})")  # Debugging print

    # Show the car availability frame and hide the admin panel
    car_availability_frame.pack(fill=tk.BOTH, expand=True)
    admin_frame.pack_forget()

    # Clear previous entries in the treeview
    for row in car_tree.get_children():
        car_tree.delete(row)

    try:
        # Connect to the database and fetch cars associated with the AdminID
        conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM CarList WHERE AdminID = ?
        """, (admin_id,))
        rows = cursor.fetchall()

        # Insert fetched data into the treeview
        if rows:
            for row in rows:
                car_tree.insert("", tk.END, values=row)
        else:
            print(f"No cars found for AdminID {admin_id}.")  # Debugging

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Show the car availability frame and hide the admin panel
    car_availability_frame.pack(fill=tk.BOTH, expand=True)
    admin_frame.pack_forget()

    # Clear previous entries in the treeview
    for row in car_tree.get_children():
        car_tree.delete(row)

    try:
        conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
        cursor = conn.cursor()

        if is_superadmin:
            # Fetch all cars for SuperAdmin
            cursor.execute("SELECT * FROM CarList")
        else:
            # Fetch cars associated with the logged-in AdminID
            cursor.execute("SELECT * FROM CarList WHERE AdminID = ?", (admin_id,))

        rows = cursor.fetchall()

        # Insert fetched data into the treeview
        if rows:
            for row in rows:
                car_tree.insert("", tk.END, values=row)
        else:
            print(f"No cars found for Admin ID: {admin_id}.")  # Debugging

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


def display_agencies_frame():
    # Retrieve the logged-in admin's session data
    admin_session = Session.get_admin_session()
    if not admin_session or "SuperAdmin" not in admin_session:
        messagebox.showerror("Access Denied", "You must be logged in as a SuperAdmin to manage agencies.")
        return

    is_superadmin = admin_session.get("SuperAdmin", False)  # Check if the admin is a SuperAdmin

    if not is_superadmin:
        messagebox.showerror("Access Denied", "Only SuperAdmin can manage agencies.")
        return

    # Proceed to display the agencies frame for SuperAdmin
    print(f"Access granted to SuperAdmin: {admin_session['username']}")  # Debugging print

    admin_frame.pack_forget()  # Hide admin panel
    agencies_frame.pack(fill=tk.BOTH, expand=True)  # Show the agencies frame

    # Clear previous entries from Agency Treeview
    for row in agency_tree.get_children():
        agency_tree.delete(row)

    # Fetch data from the database
    conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
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
            conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CarList WHERE CarID=?", (car_id,))  # Corrected the variable name to car_id
            conn.commit()  # Ensure changes are committed to the database
            conn.close()  # Always close the connection

            # Now that the car has been deleted from the database, remove it from the Treeview
            car_tree.delete(selected_item)

            # Refresh the car availability list to reflect the deletion
            display_car_availability()  # This function will re-query the database and update the Treeview

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
            conn = sqlite3.connect("Carmala.db")  # Replace with your actual database path
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
        conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
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
    # Create a new window for adding a car
    add_car_window = tk.Toplevel(root)
    add_car_window.title("Add New Car")
    add_car_window.geometry("600x900")

    # Create form labels and entry fields for car details
    tk.Label(add_car_window, text="Car Name:").pack(pady=5)
    entry_car_name = tk.Entry(add_car_window, width=40)
    entry_car_name.pack(pady=5)

    tk.Label(add_car_window, text="Car Location:").pack(pady=5)
    entry_car_location = tk.Entry(add_car_window, width=40)
    entry_car_location.pack(pady=5)

    tk.Label(add_car_window, text="Car Capacity:").pack(pady=5)
    entry_car_capacity = tk.Entry(add_car_window, width=40)
    entry_car_capacity.pack(pady=5)

    tk.Label(add_car_window, text="Car Fuel Type:").pack(pady=5)
    entry_car_fueltype = tk.Entry(add_car_window, width=40)
    entry_car_fueltype.pack(pady=5)

    tk.Label(add_car_window, text="Car Transmission:").pack(pady=5)
    entry_car_transmission = tk.Entry(add_car_window, width=40)
    entry_car_transmission.pack(pady=5)

    tk.Label(add_car_window, text="Car Features:").pack(pady=5)
    entry_car_features = tk.Entry(add_car_window, width=40)
    entry_car_features.pack(pady=5)

    tk.Label(add_car_window, text="Car Price:").pack(pady=5)
    entry_car_price = tk.Entry(add_car_window, width=40)
    entry_car_price.pack(pady=5)

    tk.Label(add_car_window, text="Car Image URL:").pack(pady=5)
    entry_car_image = tk.Entry(add_car_window, width=40)
    entry_car_image.pack(pady=5)

    # Add Car Colour field
    tk.Label(add_car_window, text="Car Colour:").pack(pady=5)
    entry_car_color = tk.Entry(add_car_window, width=40)
    entry_car_color.pack(pady=5)

    # Add Car Type field
    tk.Label(add_car_window, text="Car Type:").pack(pady=5)
    entry_car_type = tk.Entry(add_car_window, width=40)
    entry_car_type.pack(pady=5)

    # Submit button to add the car
    submit_button = tk.Button(add_car_window, text="Add Car", command=lambda: add_car(
        entry_car_name.get(),
        entry_car_location.get(),
        entry_car_capacity.get(),
        entry_car_fueltype.get(),
        entry_car_transmission.get(),
        entry_car_features.get(),
        entry_car_price.get(),
        entry_car_image.get(),
        entry_car_color.get(),   # Pass the CarColour field value
        entry_car_type.get(),    # Pass the CarType field value
        add_car_window           # Pass the window to close it after success
    ))
    submit_button.pack(pady=20)


def logout():
    clear_admin_session()
    messagebox.showinfo("Logout", "You have been logged out.")
    os.system("python Login.py")  # Redirect to the login page
    exit()



def add_car(name, location, capacity, fueltype, transmission, features, price, image_url, car_color, car_type, window):
    admin_session = get_admin_session()
    if not admin_session:
        messagebox.showerror("Error", "You must be logged in as an admin to add cars.")
        return

    admin_id = admin_session["admin_id"]  # Get the AdminID from the session

    try:
        conn = sqlite3.connect("Carmala.db")
        cursor = conn.cursor()

        # Insert new car with AdminID, CarColour, and CarType
        cursor.execute("""
            INSERT INTO CarList (CarName, CarLocation, CarCapacity, CarFueltype, CarTransmission, CarFeatures, CarPrice, CarImage, CarColour, CarType, AdminID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, location, capacity, fueltype, transmission, features, price, image_url, car_color, car_type, admin_id))

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
    edit_car_window.geometry("600x700")

    # Create form labels and entry fields pre-filled with the selected car data
    fields = [
        ("Car Name", car_data[1]), ("Car Location", car_data[2]), ("Car Capacity", car_data[3]),
        ("Car Fuel Type", car_data[4]), ("Car Transmission", car_data[5]), ("Car Features", car_data[6]),
        ("Car Price", car_data[7]), ("Car Image URL", car_data[8]), ("Car Colour", car_data[9]), ("Car Type", car_data[10])
    ]

    entries = []
    for label, value in fields:
        tk.Label(edit_car_window, text=f"{label}:").pack(pady=5)
        entry = tk.Entry(edit_car_window, width=40)
        entry.pack(pady=5)
        entry.insert(0, value)
        entries.append(entry)

    # Add a save button to save the changes
    submit_button = tk.Button(edit_car_window, text="Save Changes", command=lambda: edit_car(
        car_data[0],  # CarID
        entries[0].get(),  # CarName
        entries[1].get(),  # CarLocation
        entries[2].get(),  # CarCapacity
        entries[3].get(),  # CarFuelType
        entries[4].get(),  # CarTransmission
        entries[5].get(),  # CarFeatures
        entries[6].get(),  # CarPrice
        entries[7].get(),  # CarImage
        entries[8].get(),  # CarColour
        entries[9].get(),  # CarType
        edit_car_window   # Close the window after successful edit
    ))
    submit_button.pack(pady=20)


def edit_car(car_id, name, location, capacity, fueltype, transmission, features, price, image, color, car_type, window):
    # Update the car details in the database
    conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
    cursor = conn.cursor()

    # Execute update query
    cursor.execute("""
        UPDATE CarList SET 
        CarName = ?, CarLocation = ?, CarCapacity = ?, CarFueltype = ?, CarTransmission = ?, 
        CarFeatures = ?, CarPrice = ?, CarImage = ?, CarColour = ?, CarType = ?
        WHERE CarID = ?
    """, (name, location, capacity, fueltype, transmission, features, price, image, color, car_type, car_id))

    conn.commit()
    conn.close()

    # Refresh the car tree view after update
    display_car_availability()

    # Close the edit car window
    window.destroy()

    messagebox.showinfo("Edit Car", "Car details updated successfully.")



def display_pending_bookings():
    # Retrieve the logged-in admin's session data
    admin_session = Session.get_admin_session()
    if not admin_session or "admin_id" not in admin_session:
        messagebox.showerror("Error", "You must be logged in as an admin to view pending bookings.")
        return

    admin_id = admin_session["admin_id"]  # Retrieve AdminID from session
    is_superadmin = admin_session.get("SuperAdmin", False)  # Check if the admin is a SuperAdmin
    print(f"Displaying pending bookings for Admin ID: {admin_id} (SuperAdmin: {is_superadmin})")  # Debugging print

    # Show the pending bookings frame and hide the admin panel
    pending_bookings_frame.pack(fill=tk.BOTH, expand=True)
    admin_frame.pack_forget()

    # Clear previous entries in the treeview
    for row in pending_bookings_tree.get_children():
        pending_bookings_tree.delete(row)

    try:
        conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
        cursor = conn.cursor()

        # SuperAdmin can view all pending bookings
        if is_superadmin:
            cursor.execute("""
                SELECT 
                    b.BookingID, b.UserID, b.CarID, c.CarName, 
                    b.PickupDate, b.DropoffDate, b.BookingStatus
                FROM Booking b
                LEFT JOIN CarList c ON b.CarID = c.CarID
                WHERE b.BookingStatus = 'Pending'
            """)
        else:
            # Regular admin can view only their bookings
            cursor.execute("""
                SELECT 
                    b.BookingID, b.UserID, b.CarID, c.CarName, 
                    b.PickupDate, b.DropoffDate, b.BookingStatus
                FROM Booking b
                LEFT JOIN CarList c ON b.CarID = c.CarID
                WHERE b.BookingStatus = 'Pending' AND b.AdminID = ?
            """, (admin_id,))

        rows = cursor.fetchall()

        # Insert data into the treeview
        for row in rows:
            pending_bookings_tree.insert("", tk.END, values=row)

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


def open_feedback_page():
    # Check if the admin is logged in
    admin_session = Session.get_admin_session()
    if not admin_session:
        messagebox.showerror("Error", "Admin not logged in.")
        return

    admin_id = admin_session["admin_id"]
    is_superadmin = admin_session.get("SuperAdmin", False)  # Check if the admin is a SuperAdmin
    print(f"Opening feedback page for Admin ID: {admin_id} (SuperAdmin: {is_superadmin})")  # Debugging print

    # Fetch customer feedback
    fetch_customer_feedback(admin_id, is_superadmin)

def fetch_customer_feedback(admin_id, is_superadmin):
    try:
        conn = sqlite3.connect('Carmala.db')  # Replace with your actual database path
        cursor = conn.cursor()

        # SuperAdmin can view all feedback
        if is_superadmin:
            cursor.execute("""
                SELECT r.RatingID, r.UserID, c.CarName, r.Stars, r.Comment, r.AdminID, r.CarID
                FROM Rating r
                LEFT JOIN CarList c ON r.CarID = c.CarID
            """)
        else:
            # Regular admin can view feedback specific to their AdminID
            cursor.execute("""
                SELECT r.RatingID, r.UserID, c.CarName, r.Stars, r.Comment, r.AdminID, r.CarID
                FROM Rating r
                LEFT JOIN CarList c ON r.CarID = c.CarID
                WHERE r.AdminID = ?
            """, (admin_id,))

        rows = cursor.fetchall()
        if rows:
            # Pass the feedback data to display_feedback
            display_feedback(rows)
        else:
            messagebox.showinfo("No Feedback", "No customer feedback available.")

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def display_feedback(feedback_data):
    # Clear any existing content on the main page
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1280x700")

    # Create a frame for the feedback page
    feedback_frame = tk.Frame(root)
    feedback_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Page title
    tk.Label(feedback_frame, text="Customer Feedback", font=("Arial", 20, "bold")).pack(pady=10)

    # Create a frame for filter controls
    filter_frame = tk.Frame(feedback_frame)
    filter_frame.pack(fill=tk.X, padx=10, pady=5)

    # Label for Stars filter
    tk.Label(filter_frame, text="Filter by Stars:").pack(side=tk.LEFT, padx=5)

    # Dropdown menu for selecting stars
    star_filter_var = tk.StringVar(value="All")  # Default value
    star_dropdown = ttk.Combobox(filter_frame, textvariable=star_filter_var, state="readonly")
    star_dropdown['values'] = ["All", "1", "2", "3", "4", "5"]  # All options for stars
    star_dropdown.pack(side=tk.LEFT, padx=5)

    # Apply filter button
    def apply_filter():
        selected_star = star_filter_var.get()

        # Clear the Treeview
        for row in feedback_tree.get_children():
            feedback_tree.delete(row)

        # Filter feedback data
        filtered_data = (
            feedback_data if selected_star == "All"
            else [row for row in feedback_data if int(row[3]) == int(selected_star)]  # Adjusted for Stars index
        )

        # Insert filtered data into the Treeview
        for row in filtered_data:
            feedback_tree.insert("", tk.END, values=row)

    tk.Button(filter_frame, text="Apply Filter", command=apply_filter).pack(side=tk.LEFT, padx=10)

    # Back button to return to admin panel
    back_button = tk.Button(feedback_frame, text="Back",
                            command=lambda: [root.destroy(), subprocess.run(["python", "adminpage.py"])],  # Destroy and relaunch adminpage.py
                            bg="#1572D3",  fg="white", font=("Poppins", 12, "bold"))
    back_button.pack(side=tk.BOTTOM, pady=10)  # Place it at the bottom of the feedback_frame

    # Create a treeview for displaying feedback
    feedback_tree = ttk.Treeview(feedback_frame, columns=("RatingID", "UserID", "CarName", "Stars", "Comment", "AdminID", "CarID"), show="headings")
    feedback_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Define column headings
    feedback_tree.heading("RatingID", text="Rating ID")
    feedback_tree.heading("UserID", text="User ID")
    feedback_tree.heading("CarName", text="Car Name")
    feedback_tree.heading("Stars", text="Stars")
    feedback_tree.heading("Comment", text="Comment")
    feedback_tree.heading("AdminID", text="Admin ID")
    feedback_tree.heading("CarID", text="Car ID")

    feedback_tree.column("RatingID", width=80)
    feedback_tree.column("UserID", width=80)
    feedback_tree.column("CarName", width=80)
    feedback_tree.column("Stars", width=80)
    feedback_tree.column("Comment", width=300)
    feedback_tree.column("AdminID", width=80)
    feedback_tree.column("CarID", width=80)

    # Insert rows into the Treeview
    for row in feedback_data:
        feedback_tree.insert("", tk.END, values=row)





# --- MAIN WINDOW SETUP --- #
root = tk.Tk()
root.title("Login Page")
root.geometry('1200x700')

# Main frame for layout
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# --- LOGIN PAGE --- #
login_frame = tk.Frame(main_frame, bg='#F1F1F1')
login_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Right side image (during login)
right_frame = tk.Frame(main_frame, bg='#F1F1F1', width=400)
right_frame.pack(fill=tk.Y, side=tk.RIGHT)
image_path = r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-24 200101.png"# Add your path
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

        # Create a new Toplevel window for the rejection reason
        reason_window = Toplevel()
        reason_window.title("Enter Rejection Reason")
        reason_window.geometry("400x300")  # Adjust size as needed

        # Add a Text widget (chat box-style) for the admin to type the reason
        reason_text = Text(reason_window, wrap="word", height=10)
        reason_text.pack(padx=10, pady=10, expand=True)

        # Add a button to submit the rejection reason
        def submit_reason():
            reason = reason_text.get("1.0", "end-1c").strip()  # Get the text input
            if not reason:
                messagebox.showwarning("Input Required", "Rejection reason cannot be empty.")
                return

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

                    # Update the BookingStatus in the Booking table to 'Rejected'
                    cursor.execute("UPDATE Booking SET BookingStatus = 'Rejected' WHERE BookingID = ?", (booking_id,))
                    conn.commit()

                    # Create the email content
                    subject = "Booking Rejected"
                    message = f"""
                    Dear Valued Customer,

                    We regret to inform you that your booking has been rejected.

                    *Booking Details:*
                    - Car: {car_name}
                    - Pickup Date: {pickup_date_formatted}
                    - Dropoff Date: {dropoff_date_formatted}
                    - Status: Rejected

                    *Reason for Rejection:*
                    {reason}

                    If you have any questions or need assistance, please contact our support team.

                    Best regards,
                    Carmala Team
                    """

                    # Send email notification
                    send_email_notification(user_email, subject, message)

                    # Refresh the pending bookings list
                    display_pending_bookings()
                    messagebox.showinfo("Success", "Booking rejected successfully!")

                    reason_window.destroy()  # Close the reason input window
                else:
                    messagebox.showerror("Error", "User email or car details not found.")

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

            finally:
                conn.close()

        # Add a button to submit the reason and process the rejection
        submit_button = Button(reason_window, text="Submit Rejection", command=submit_reason)
        submit_button.pack(pady=10)

    else:
        messagebox.showerror("Error", "Please select a booking to reject.")



# Function to handle double-click event on pending bookings
def on_pending_booking_double_click(event):
    # Get selected item
    selected_item = pending_bookings_tree.selection()
    if not selected_item:
        return

    booking_id = pending_bookings_tree.item(selected_item, 'values')[0]
    user_id = pending_bookings_tree.item(selected_item, 'values')[1]

    display_user_details(user_id)  # Call the function to display user details



# Function to handle double-click event on pending bookings
def on_pending_booking_double_click(event):
    # Get selected item
    selected_item = pending_bookings_tree.selection()
    if not selected_item:
        return

    booking_id = pending_bookings_tree.item(selected_item, 'values')[0]  # Getting BookingID
    user_id = pending_bookings_tree.item(selected_item, 'values')[1]  # Getting UserID

    display_user_details(user_id)  # Call the function to display user details

# Function to display user details in a new window
def display_user_details(user_id):
    try:
        conn = sqlite3.connect("Carmala.db")  # Replace with your actual DB path
        cursor = conn.cursor()

        # Query to fetch user details by UserID
        cursor.execute("""
            SELECT UserName, IdentificationNumber, DrivingLicense, ProfilePicture, 
                   Email, Country, Gender
            FROM UserAccount
            WHERE UserID = ?
        """, (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            user_name, id_number, driving_license, profile_picture, email, country, gender = user_data

            # Create a new window to display user details
            user_window = tk.Toplevel(root)
            user_window.title(f"User Details - {user_name}")
            user_window.geometry("600x500")

            # Display the user details
            tk.Label(user_window, text=f"User Name: {user_name}").pack(pady=5)
            tk.Label(user_window, text=f"Identification Number: {id_number}").pack(pady=5)
            tk.Label(user_window, text=f"Email: {email}").pack(pady=5)
            tk.Label(user_window, text=f"Country: {country}").pack(pady=5)
            tk.Label(user_window, text=f"Gender: {gender}").pack(pady=5)

            # Display Profile Picture if available
            if profile_picture:
                image = Image.open(io.BytesIO(profile_picture))
                image.thumbnail((150, 150))  # Resize image
                profile_img = ImageTk.PhotoImage(image)

                profile_label = tk.Label(user_window, image=profile_img)
                profile_label.image = profile_img  # Keep a reference to the image
                profile_label.pack(pady=5)

            # Display Driving License Image if available
            if driving_license:
                driving_license_img = Image.open(io.BytesIO(driving_license))
                driving_license_img.thumbnail((150, 150))  # Resize image
                driving_license_photo = ImageTk.PhotoImage(driving_license_img)

                driving_license_label = tk.Label(user_window, image=driving_license_photo)
                driving_license_label.image = driving_license_photo  # Keep reference
                driving_license_label.pack(pady=5)

            # Close button
            tk.Button(user_window, text="Close", command=user_window.destroy).pack(pady=10)

        else:
            messagebox.showinfo("No User Data", "No user details found.")

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Function to display user details in a new window
def display_user_details(user_id):
    try:
        conn = sqlite3.connect("Carmala.db")
        cursor = conn.cursor()

        # Query to fetch user details by UserID
        cursor.execute("""
            SELECT UserName, IdentificationNumber, DrivingLicense, ProfilePicture, 
                   Email, Country, Gender
            FROM UserAccount
            WHERE UserID = ?
        """, (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            user_name, id_number, driving_license, profile_picture, email, country, gender = user_data

            # Create a new window to display user details
            user_window = tk.Toplevel(root)
            user_window.title(f"User Details - {user_name}")
            user_window.geometry("600x500")

            # Display the user details
            tk.Label(user_window, text=f"User Name: {user_name}").pack(pady=5)
            tk.Label(user_window, text=f"Identification Number: {id_number}").pack(pady=5)
            tk.Label(user_window, text=f"Email: {email}").pack(pady=5)
            tk.Label(user_window, text=f"Country: {country}").pack(pady=5)
            tk.Label(user_window, text=f"Gender: {gender}").pack(pady=5)

            # Display Profile Picture if available
            if profile_picture:
                image = Image.open(io.BytesIO(profile_picture))
                image.thumbnail((150, 150))  # Resize image
                profile_img = ImageTk.PhotoImage(image)

                profile_label = tk.Label(user_window, image=profile_img)
                profile_label.image = profile_img  # Keep a reference to the image
                profile_label.pack(pady=5)

            # Display Driving License Image if available
            if driving_license:
                driving_license_img = Image.open(io.BytesIO(driving_license))
                driving_license_img.thumbnail((150, 150))  # Resize image
                driving_license_photo = ImageTk.PhotoImage(driving_license_img)

                driving_license_label = tk.Label(user_window, image=driving_license_photo)
                driving_license_label.image = driving_license_photo  # Keep reference
                driving_license_label.pack(pady=5)

            # Close button
            tk.Button(user_window, text="Close",  fg="white", font=("Poppins", 12, "bold"),command=user_window.destroy).pack(pady=10)

        else:
            messagebox.showinfo("No User Data", "No user details found.")

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def open_manage_users_page():
    admin_session = Session.get_admin_session()  # Get current admin session
    if not admin_session or not admin_session.get("SuperAdmin", False):  # Check if Superadmin
        messagebox.showerror("Access Denied", "Only Superadmin can manage users.")
        return

    # Create a new window for managing users
    manage_users_window = tk.Toplevel(root)
    manage_users_window.title("Manage Users")
    manage_users_window.geometry("800x600")

    # Create a treeview to display users
    user_tree = ttk.Treeview(manage_users_window, columns=("UserID", "UserName", "Email", "Country", "Gender"), show="headings")
    user_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    # Bind double-click event to view user details
    user_tree.bind("<Double-1>", lambda event: on_user_double_click(event, user_tree))
    user_tree.heading("UserID", text="User ID")
    user_tree.heading("UserName", text="User Name")
    user_tree.heading("Email", text="Email")
    user_tree.heading("Country", text="Country")
    user_tree.heading("Gender", text="Gender")

    # Fetch and insert user data into the treeview
    try:
        conn = sqlite3.connect("Carmala.db")
        cursor = conn.cursor()

        cursor.execute("SELECT UserID, UserName, Email, Country, Gender FROM UserAccount")
        users = cursor.fetchall()

        for user in users:
            user_tree.insert("", tk.END, values=user)

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Add a "Ban User" button below the treeview
    ban_button = tk.Button(manage_users_window, text="Ban User",bg="#1572D3", fg="white", font=("Poppins", 12, "bold"), command=lambda: ban_user(user_tree))
    ban_button.pack(pady=10)
def on_user_double_click(event, user_tree):
    # Get the selected item
    selected_item = user_tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a user to view details.")
        return

    # Get user data from the selected row
    user_data = user_tree.item(selected_item, "values")
    user_id = user_data[0]  # Assuming UserID is the first column

    # Call the function to display user details
    display_user_details(user_id)



# Function to ban a user and send an email with the reason
def ban_user(user_tree):
    selected_item = user_tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a user to ban.")
        return

    user_id = user_tree.item(selected_item)['values'][0]  # Getting UserID
    user_name = user_tree.item(selected_item)['values'][1]  # Getting User Name
    user_email = user_tree.item(selected_item)['values'][2]  # Getting User Email

    # Create a window with a Text widget for entering ban reason
    ban_window = tk.Toplevel(root)
    ban_window.title("Ban User")
    ban_window.geometry("400x300")

    tk.Label(ban_window, text="Enter the reason for banning the user:").pack(pady=10)

    # Text widget for reason
    ban_reason_text = tk.Text(ban_window, height=5, width=40)
    ban_reason_text.pack(pady=10)

    # Submit button to confirm ban
    submit_button = tk.Button(ban_window, text="Ban User",bg="#1572D3", fg="white", font=("Poppins", 12, "bold"), command=lambda: confirm_ban(user_id, user_name, user_email, ban_reason_text.get("1.0", tk.END), ban_window))
    submit_button.pack(pady=10)

# Function to confirm the ban and perform actions
def confirm_ban(user_id, user_name, user_email, ban_reason, ban_window):
    if not ban_reason.strip():
        messagebox.showwarning("No Reason", "Please provide a reason for banning the user.")
        return

    try:
        # Delete the user record from the database
        conn = sqlite3.connect("Carmala.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM UserAccount WHERE UserID = ?", (user_id,))
        conn.commit()
        conn.close()

        # Send an email to the user
        send_ban_email(user_email, user_name, ban_reason)

        messagebox.showinfo("User Banned", f"User {user_name} has been banned successfully.")

        # Refresh the user treeview to reflect changes
        open_manage_users_page()

        ban_window.destroy()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Function to send the ban email to the user
def send_ban_email(user_email, user_name, ban_reason):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = admin_email = "killerpill585@gmail.com"
        sender_password = "oxey jnwo qybz etmg"

        message = MIMEMultipart()
        message["Subject"] = "Your Account Has Been Banned"
        message["From"] = sender_email
        message["To"] = user_email
        body = f"Dear {user_name},\n\nYour account has been banned for the following reason:\n\n{ban_reason}\n\nIf you have any questions, please contact support."
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, message.as_string())
        server.quit()

    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send ban email: {e}")

def save_chart_as_image(fig):
    """
    Save a Matplotlib figure to a PNG image and return as a PIL Image object.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    return Image.open(buf)


def print_charts_to_pdf():
    """
    Generate a PDF report including the charts and allow the user to save it.
    """
    try:
        # Open a Save As dialog for the user to choose the file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Report As"
        )
        if not file_path:
            return  # User canceled the dialog

        # Initialize a PDF canvas
        c = canvas.Canvas(file_path, pagesize=letter)

        # Add title to the PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 750, "Admin Dashboard Report")

        y_position = 700  # Initial Y position for the first chart

        # Booking Statistics Chart
        total, approved, rejected = get_statistics_data()
        fig1 = Figure(figsize=(4, 3), dpi=100)
        ax1 = fig1.add_subplot(111)
        labels = ['Total', 'Approved', 'Rejected']
        values = [total, approved, rejected]
        colors = ['#4CAF50', '#2196F3', '#F44336']
        bars = ax1.bar(labels, values, color=colors)
        ax1.set_title("Booking Statistics")
        ax1.set_ylabel("Number of Bookings")
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        img1 = save_chart_as_image(fig1)
        img1.save("booking_chart_temp.png")  # Save image temporarily
        c.drawImage("booking_chart_temp.png", 50, y_position - 300, width=400, height=300)
        y_position -= 350

        # Revenue Statistics Chart
        total_revenue, monthly_revenue = get_revenue_statistics()
        fig2 = Figure(figsize=(4, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        months = [row[0] for row in monthly_revenue]
        revenues = [row[1] for row in monthly_revenue]
        colors = ['#FFD700' for _ in months]
        bars = ax2.bar(months, revenues, color=colors)
        ax2.set_title("Revenue Statistics")
        ax2.set_xlabel("Month")
        ax2.set_ylabel("Revenue ($)")
        ax2.tick_params(axis='x', rotation=45, labelsize=8)
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f'${int(height):,}', xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        img2 = save_chart_as_image(fig2)
        img2.save("revenue_chart_temp.png")  # Save image temporarily
        c.drawImage("revenue_chart_temp.png", 50, y_position - 300, width=400, height=300)
        y_position -= 350

        # Car Usage Distribution Pie Chart
        labels, data = get_car_usage_data()
        if labels and data:
            fig3 = Figure(figsize=(5, 3), dpi=100)  # Wider for pie chart legend
            ax3 = fig3.add_subplot(111)
            colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4CAF50', '#2196F3', '#F44336']
            while len(colors) < len(labels):
                colors.append("#" + "".join(random.choice("0123456789ABCDEF") for _ in range(6)))
            wedges, texts, autotexts = ax3.pie(data, labels=None, autopct='%1.0f%%', startangle=90, colors=colors)
            ax3.legend(handles=[Patch(facecolor=colors[i], label=labels[i]) for i in range(len(labels))],
                       title="Cars", loc='center left', bbox_to_anchor=(1, 0.5))
            ax3.set_title("Car Usage Distribution")
            img3 = save_chart_as_image(fig3)
            img3.save("car_usage_chart_temp.png")  # Save image temporarily
            c.drawImage("car_usage_chart_temp.png", 50, y_position - 300, width=400, height=300)

        # Save the PDF and clean up
        c.save()
        messagebox.showinfo("Success", f"Report saved as {file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")


# --- PENDING BOOKINGS PAGE --- #
pending_bookings_frame = tk.Frame(main_frame, bg='#F1F1F1')
back_button = tk.Button(pending_bookings_frame, text="Back", command=lambda: [pending_bookings_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", fg="white", font=("Poppins", 12, "bold"))
back_button.pack(pady=10)

# Define columns for the Pending Bookings Treeview
pending_bookings_columns = ("BookingID", "UserID", "CarID", "CarName", "PickupDate", "DropoffDate", "BookingStatus")
pending_bookings_tree = ttk.Treeview(pending_bookings_frame, columns=pending_bookings_columns, show="headings")
pending_bookings_tree.heading("BookingID", text="Booking ID")
pending_bookings_tree.heading("UserID", text="User ID")
pending_bookings_tree.heading("CarID", text="Car ID")
pending_bookings_tree.heading("CarName", text="Car Name")
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
pending_bookings_tree.bind("<Double-1>", on_pending_booking_double_click)

# --- ADMIN PANEL --- #
admin_frame = tk.Frame(main_frame, bg='#F1F1F1')

admin_image_label = tk.Label(admin_frame)
admin_image_label.pack(fill=tk.BOTH, expand=True)

# Admin panel buttons
button_pending_bookings = tk.Button(admin_frame,bg="#28A1F8",fg = "white", text="Pending Bookings", font=("Poppins", 12, "bold"), command=display_pending_bookings)
button_pending_bookings.bind("<Enter>", lambda event: on_hover(button_pending_bookings, "#1058A7"))
button_pending_bookings.bind("<Leave>", lambda event: on_leave(button_pending_bookings, "#28A1F8"))

button_feedback = tk.Button(admin_frame, bg="#28A1F8",fg = "white",text="Customer Feedback", font=("Poppins", 12, "bold"), command=open_feedback_page)
button_feedback.bind("<Enter>", lambda event: on_hover(button_feedback, "#1058A7"))
button_feedback.bind("<Leave>", lambda event: on_leave(button_feedback, "#28A1F8"))

button_manage_cars = tk.Button(admin_frame, bg="#28A1F8",fg = "white",text="Show Cars", font=("Poppins", 12, "bold"), command=display_car_availability)
button_manage_cars.bind("<Enter>", lambda event: on_hover(button_manage_cars, "#1058A7"))
button_manage_cars.bind("<Leave>", lambda event: on_leave(button_manage_cars, "#28A1F8"))

button_agencies = tk.Button(admin_frame, bg="#28A1F8",fg = "white",text="Agencies", font=("Poppins", 12, "bold"), command=display_agencies_frame)
button_agencies.bind("<Enter>", lambda event: on_hover(button_agencies, "#1058A7"))
button_agencies.bind("<Leave>", lambda event: on_leave(button_agencies, "#28A1F8"))

button_manage_users  = tk.Button(admin_frame, bg="#28A1F8",fg = "white",text="Manage Users", font=("Poppins", 12, "bold"), command=open_manage_users_page)
button_manage_users .bind("<Enter>", lambda event: on_hover(button_manage_users , "#1058A7"))
button_manage_users .bind("<Leave>", lambda event: on_leave(button_manage_users , "#28A1F8"))

button_print= tk.Button(admin_frame, text="Print Report",bg="#28A1F8",fg = "white", font=("Poppins", 12, "bold"), command=print_charts_to_pdf)
button_manage_users .bind("<Enter>", lambda event: on_hover(button_manage_users , "#1058A7"))
button_manage_users .bind("<Leave>", lambda event: on_leave(button_manage_users , "#28A1F8"))



logout_button = tk.Button(admin_frame,bg="#28A1F8",fg = "white", text="Logout", font=("Poppins", 12, "bold"), command=logout)
logout_button.bind("<Enter>", lambda event: on_hover(logout_button, "#1058A7"))
logout_button.bind("<Leave>", lambda event: on_leave(logout_button, "#28A1F8"))
logout_button.place(x=10, y=640, width=180, height=40)



# --- CAR AVAILABILITY PAGE --- #
car_availability_frame = tk.Frame(main_frame, bg='#F1F1F1')
back_button = tk.Button(car_availability_frame, text="Back", command=lambda: [car_availability_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", fg="white", font=("Poppins", 12, "bold"))
back_button.pack(pady=10)
add_car_button = tk.Button(car_availability_frame, text="Add Car", command=open_add_car_form, bg="#1572D3", fg="white", font=("Poppins", 12, "bold"))
add_car_button.pack(pady=10)

# Edit car button in the Car Availability frame (adjust size and color)
button_edit_car = tk.Button(car_availability_frame,text="Edit Car",font=("Poppins", 12, "bold"),bg="green", fg="white",command=lambda: open_edit_car_form())
button_edit_car.pack(pady=10)


# Separate Treeview for car availability
car_columns = ("CarID", "CarName", "CarLocation", "CarCapacity","CarFueltype","CarTransmission","CarFeatures","CarPrice","CarImage","AdminID")
car_tree = ttk.Treeview(car_availability_frame, columns=car_columns, show="headings")
# Add a delete button in the car_availability_frame
delete_button = tk.Button(car_availability_frame, text="Delete Selected", command=delete_selected_row, bg="#FF6347", fg="white", font=("Poppins", 12, "bold"))
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
back_button = tk.Button(agencies_frame, text="Back", command=lambda: [agencies_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", fg="white", font=("Poppins", 12, "bold"))
back_button.pack(pady=10)
agencies_frame = tk.Frame(main_frame, bg='#F1F1F1')
back_button = tk.Button(agencies_frame, text="Back", command=lambda: [agencies_frame.pack_forget(), admin_frame.pack(fill=tk.BOTH, expand=True)], bg="#1572D3", fg="white", font=("Poppins", 12, "bold"))
back_button.pack(pady=10)

# Delete Button for agencies
delete_agency_button = tk.Button(agencies_frame, text="Delete Selected", command=delete_selected_agency, bg="#FF6347",fg="white", font=("Poppins", 12, "bold"))
delete_agency_button.pack(pady=10)
# Add Button for agencies
add_agency_button = tk.Button(agencies_frame, text="Add New Agency", command=open_add_agency_form, bg="#32CD32",fg="white", font=("Poppins", 12, "bold"))
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
approve_button = tk.Button(pending_bookings_frame, text="Approve Booking", command=approve_booking, bg="green", font=("Poppins", 12, "bold"), fg="white")
approve_button.pack(side=tk.LEFT, padx=20, pady=10)

reject_button = tk.Button(pending_bookings_frame, text="Reject Booking", command=reject_booking, bg="red", font=("Poppins", 12, "bold"), fg="white")
reject_button.pack(side=tk.LEFT, padx=20, pady=10)

# Update the "Pending Bookings" button to call this function
button_pending_bookings.config(command=display_pending_bookings)


open_admin_panel()

root.mainloop()
