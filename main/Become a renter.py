import customtkinter as ctk
from PIL import Image, ImageTk
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
    root.destroy()


# Function to change button color on hover
def on_hover(button, color):
    button.configure(fg_color=color)

def on_leave(button, color):
    button.configure(fg_color=color)


# Function to scroll back to the top
def scroll_to_top():
    canvas.yview_moveto(0)  # Moves the scrollbar to the top position


# Create a window with a specific geometry
ctk.set_appearance_mode("light")  # Set appearance mode (light/dark)
ctk.set_default_color_theme("blue")  # Set default color theme

root = ctk.CTk()
root.title("Become a renter")
root.geometry("1030x620")
root.resizable(False, False)


# Set up a frame for the canvas and scrollbar
frame = ctk.CTkFrame(root)
frame.pack(fill=ctk.BOTH, expand=True)

# Create a canvas
canvas = ctk.CTkCanvas(frame)
canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

# Add a scrollbar
scrollbar = ctk.CTkScrollbar(frame, command=canvas.yview)
scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

# Configure canvas scrolling
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create the "Back to Home" button without extra space and transparent background
home_button = ctk.CTkButton(root,text="Back to Home",font=("Poppins", 12, "bold"),command=open_home,hover_color="#1572D3",cursor="hand2",  height=20)
home_button.bind("<Enter>", lambda event: on_hover(home_button, "#1058A7"))
home_button.bind("<Leave>", lambda event: on_leave(home_button, "#1572D3"))
canvas.create_window(50, 40, anchor="nw", window=home_button)

# Load the images
image_paths = [
    "Carmala cars/become a renter 1.png",
    "Carmala cars/become a renter 2.png",
    "Carmala cars/become a renter 3.png",
    "Carmala cars/become a renter 4.png"
]

loaded_images = []

# Set each image to fill the window size (1280x780)
window_width = 1280
window_height = 710

for idx, image_path in enumerate(image_paths):
    img = Image.open(image_path)
    # Resize image to match window size
    img = img.resize((window_width, window_height), Image.Resampling.LANCZOS)  # Use LANCZOS for better quality
    img_tk = ImageTk.PhotoImage(img)
    loaded_images.append(img_tk)

    # Add image directly to the canvas
    canvas.create_image(0, idx * window_height, anchor="nw", image=img_tk)

# Add the "Back to Top" button without extra space and transparent background
back_to_top_button = ctk.CTkButton(root,text="Back to Top",font=("Poppins", 12, "bold"),command=scroll_to_top,hover_color="#ADD8E6",
                                   border_width=0,cursor="hand2",width=150, height=0 )
back_to_top_button.bind("<Enter>", lambda event: on_hover(back_to_top_button, "#1058A7"))
back_to_top_button.bind("<Leave>", lambda event: on_leave(back_to_top_button, "#1572D3"))
canvas.create_window(550, len(image_paths) * window_height - 70, anchor="nw", window=back_to_top_button)

# Start the main loop
root.mainloop()
