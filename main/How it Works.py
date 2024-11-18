import customtkinter as ctk
from PIL import Image, ImageTk
import Session

logged_in_user = Session.get_user_session()

if logged_in_user:
    user_id = logged_in_user.get("user_id")
    print(f"Logged in user ID: {user_id}")
else:
    print("No user is logged in.")


# Function to open the selected button
def open_home():
    root.destroy()


# Function to change button color on hover
def on_hover(button, color):
    button.configure(bg_color=color)


def on_leave(button, color):
    button.configure(bg_color=color)

# Function to scroll back to the top
def scroll_to_top():
    canvas.yview_moveto(0)  # Moves the scrollbar to the top position


# Create a window with a specific geometry
root = ctk.CTk()
root.title("How it Works")
root.geometry("1100x680")  # Set window size to 1280x780

# Set up a frame for the canvas and scrollbar using CustomTkinter
frame = ctk.CTkFrame(root)
frame.pack(fill="both", expand=True)

# Create a canvas using CustomTkinter
canvas = ctk.CTkCanvas(frame)
canvas.pack(side="left", fill="both", expand=True)

# Add a scrollbar using CustomTkinter (no 'orient' argument)
scrollbar = ctk.CTkScrollbar(frame, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure canvas scrolling
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create "Home" button without extra space and transparent background
home_button = ctk.CTkButton(
    root,
    text="Back to Home",
    font=("Poppins", 12, "bold"),
    command=open_home,
    hover_color="#1572D3",  # Light blue hover color
    border_width=0,  # Remove border
    cursor="hand2",  # Change cursor to hand on hover
    width=150,  # Set appropriate width
    height=20  # Set appropriate height
)
home_button.bind("<Enter>", lambda event: on_hover(home_button, "#1058A7"))
home_button.bind("<Leave>", lambda event: on_leave(home_button, "#1572D3"))
canvas.create_window(50, 40, anchor="nw", window=home_button)

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
image_objects = []  # Store image references to avoid garbage collection

# Set each image to fill the window size (1280x780)
window_width = 1380
window_height = 780

# Load and display images directly on the canvas using create_image
for idx, image_path in enumerate(image_paths):
    img = Image.open(image_path)
    img = img.resize((window_width, window_height))  # Resize image to fill the window
    img_tk = ImageTk.PhotoImage(img)  # Convert the image to a Tkinter-compatible photo
    loaded_images.append(img_tk)

    # Display the image directly on the canvas using create_image
    image_objects.append(img)  # Save the image reference to avoid garbage collection
    canvas.create_image(0, window_height * idx, anchor="nw", image=img_tk)

# Add the "Back to Top" button without extra space and transparent background
back_to_top_button = ctk.CTkButton(
    root,
    text="Back to Top",
    font=("Poppins", 12, "bold"),
    command=scroll_to_top,
    hover_color="#ADD8E6",  # Light blue hover color, or use the default hover color
    border_width=0,  # Remove border
    cursor="hand2",  # Change cursor to hand on hover
    width=150,  # Set to 0 to minimize width
    height=20  # Set to 0 to minimize height
)
back_to_top_button.bind("<Enter>", lambda event: on_hover(back_to_top_button, "#1058A7"))
back_to_top_button.bind("<Leave>", lambda event: on_leave(back_to_top_button, "#1572D3"))
canvas.create_window(600, len(image_paths) * window_height - 50, anchor="nw", window=back_to_top_button)

# Start the main loop
root.mainloop()
