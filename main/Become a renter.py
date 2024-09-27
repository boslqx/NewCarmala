import tkinter as tk
from tkinter import Scrollbar, Canvas
from PIL import Image, ImageTk

# Create a window with a specific geometry
root = tk.Tk()
root.title("Image Viewer with Scrollbar")
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
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-27 103340.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-27 103615.png",
    r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-27 103735.png"
]

loaded_images = []

# Set each image to fill the window size (1280x780)
window_width = 1280
window_height = 780

for image_path in image_paths:
    img = Image.open(image_path)
    img = img.resize((window_width, window_height))  # Resize image to fill the window
    img_tk = ImageTk.PhotoImage(img)
    loaded_images.append(img_tk)

    label = tk.Label(image_frame, image=img_tk)
    label.pack()  # Pack each image to be visible one at a time with scrolling

# Create a button for get started
getstarted =tk.Button(root, text = "Get Started", bg="blue",fg="white",font=("Poppins", 18))
getstarted.pack()
# Start the main loop
root.mainloop()
