import tkinter as tk
from tkinter import Scrollbar, Canvas
from PIL import Image, ImageTk

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


# Start the main loop
root.mainloop()
