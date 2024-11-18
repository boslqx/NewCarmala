import tkinter as tk
from tkinter import Scrollbar, Canvas
from PIL import Image, ImageTk
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

# Function to open the selected button
def open_home():
    process = subprocess.Popen(["python", "Home.py"])
    print("Home opened with process ID:", process.pid)

    # Delay the close of the current window
    root.after(400, root.destroy)  # Waits 300 milliseconds (1 second) before destroying

# Function to open the selected button
def open_userprofile():
    # root.destroy()
    process = subprocess.Popen(["python", "User profile.py"])
    print("User Profile opened with process ID:", process.pid)

    # Delay the close of the current window
    #root.after(1000, root.destroy)  # Waits 300 milliseconds (1 second) before destroying

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

# Function to change button color on hover
def on_hover(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color

# Create a window with a specific geometry
root = tk.Tk()
root.title("How it Works")
root.geometry("1280x780")  # Set window size to 1280x780

# Set up a frame for the canvas and scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas
canvas = Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar
scrollbar = Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure canvas scrolling
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# create home button
home_button = tk.Button(root, bg="#1572D3", text="Home", fg="white",font=("Poppins",12,"bold"), command=open_home)
home_button.bind("<Enter>", lambda event: on_hover(home_button, "#1058A7"))
home_button.bind("<Leave>", lambda event: on_leave(home_button, "#1572D3"))
canvas.create_window(200, 40, anchor="nw", window=home_button)

# create become a renter button
become_renter_button = tk.Button(root, bg="#1572D3", text="Become a Renter", fg="white",font=("Poppins",12,"bold"), command=open_becomearenter)
become_renter_button.bind("<Enter>", lambda event: on_hover(become_renter_button, "#1058A7"))
become_renter_button.bind("<Leave>", lambda event: on_leave(become_renter_button, "#1572D3"))
canvas.create_window(300, 40, anchor="nw", window=become_renter_button)

# create how it works button
how_it_works_button = tk.Button(root, bg="#1572D3", text="How It Works", fg="white",font=("Poppins",12,"bold"), command=open_howitworks)
how_it_works_button.bind("<Enter>", lambda event: on_hover(how_it_works_button, "#1058A7"))
how_it_works_button.bind("<Leave>", lambda event: on_leave(how_it_works_button, "#1572D3"))
canvas.create_window(470, 40, anchor="nw", window=how_it_works_button)

# create profile button
userprofile_button = tk.Button(root, bg="#1572D3", text="Profile", fg="white",font=("Poppins",12,"bold"), command=open_userprofile)
userprofile_button.bind("<Enter>", lambda event: on_hover(userprofile_button, "#1058A7"))
userprofile_button.bind("<Leave>", lambda event: on_leave(userprofile_button, "#1572D3"))
canvas.create_window(610, 40, anchor="nw", window=userprofile_button)

# Create another frame inside the canvas to hold the images
image_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=image_frame, anchor="nw")

# Load the images
image_paths = [
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-29 212411.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-29 212422.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-29 212430.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-29 212442.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-29 212456.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-29 212503.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-29 212510.png"
]

loaded_images = []
labels = []  # Store image labels for future reference

# Set each image to fill the window size (1280x780)
window_width = 1280
window_height = 780

for idx, image_path in enumerate(image_paths):
    img = Image.open(image_path)
    img = img.resize((window_width, window_height))  # Resize image to fill the window
    img_tk = ImageTk.PhotoImage(img)
    loaded_images.append(img_tk)

    label = tk.Label(image_frame, image=img_tk)
    label.pack()  # Pack each image to be visible one at a time with scrolling
    labels.append(label)  # Store label references

# Create the "Get Started" button
get_started_btn = tk.Button(labels[-1],bg ="#1572D3",fg = "white",text="Get Started", font=("Poppins", 16), width=21, height=2, command=open_home)

# Place the button at the bottom center of the last image
get_started_btn.place(relx=0.5, rely=0.95, anchor=tk.CENTER)


# Start the main loop
root.mainloop()
