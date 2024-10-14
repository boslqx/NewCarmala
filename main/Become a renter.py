import tkinter as tk
from tkinter import Scrollbar, Canvas
from PIL import Image, ImageTk
import subprocess

# Function to open the selected button
def open_home():
    root.destroy()
    subprocess.Popen(["python", "Home.py"])

# Function to open the selected button
def open_userprofile():
    root.destroy()
    subprocess.Popen(["python", "User profile.py"])

# Function to open the script when the "How it Works" button is clicked
def open_howitworks():
    root.destroy()
    subprocess.Popen(["python", "How it Works.py"])

# Function to open the script when the "Become a Renter" button is clicked
def open_becomearenter():
    root.destroy()
    subprocess.Popen(["python", "Become a renter.py"])

# Create a window with a specific geometry
root = tk.Tk()
root.title("Become a renter")
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
home_button = tk.Button(root, bg="#1572D3", text="Home", font=("Poppins", 12), command=open_home)
canvas.create_window(200, 40, anchor="nw", window=home_button)

# create become a renter button
become_renter_button = tk.Button(root, bg="#1572D3", text="Become a Renter", font=("Poppins", 12), command=open_becomearenter)
canvas.create_window(300, 40, anchor="nw", window=become_renter_button)

# create how it works button
how_it_works_button = tk.Button(root, bg="#1572D3", text="How It Works", font=("Poppins", 12), command=open_howitworks)
canvas.create_window(470, 40, anchor="nw", window=how_it_works_button)

# create profile button
userprofile_button = tk.Button(root, bg="#1572D3", text="Profile", font=("Poppins", 12), command=open_userprofile)
canvas.create_window(600, 40, anchor="nw", window=userprofile_button)

# Create another frame inside the canvas to hold the images
image_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=image_frame, anchor="nw")

# Load the images
image_paths = [
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-27 103340.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-27 103615.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-10-06 212255.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-10-06 212059.png"
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

# Start the main loop
root.mainloop()
