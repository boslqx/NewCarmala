import tkinter as tk
from PIL import Image, ImageTk
import subprocess

# create log out function
def logout():
    root.destroy()
    subprocess.popen(["Python","Login.py"])


# Create the main window
root = tk.Tk()
root.title("Account Login Page")
root.geometry('1280x780')

# Create a main frame for the layout
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

def open_admin_panel():
    # Hide the login frame
    main_frame.pack_forget()

    # Show the admin panel
    admin_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    # Hide the previous image (if it's on the right side or background)
    main_frame.pack_forget()

    # Load the admin-specific image and place it in the background
    admin_image_path = r"C:\Users\User\Downloads\Image (1).png" # Add your admin image path here
    admin_image = Image.open(admin_image_path)
    admin_image = admin_image.resize((1280, 780), Image.LANCZOS)
    admin_photo = ImageTk.PhotoImage(admin_image)
    admin_image_label.config(image=admin_photo)
    admin_image_label.image = admin_photo
    admin_image_label.pack(fill=tk.BOTH, expand=True)

    # Place buttons overlapping on top of the image
    place_buttons_on_image()


def place_buttons_on_image():
    # Place the side panel for buttons on top of the image
    button_statistics.place(x=65, y=155, width=180, height=40)
    button_notifications.place(x=65, y=205, width=180, height=40)
    button_feedback.place(x=65, y=255, width=180, height=40)
    button_car_availability.place(x=65, y=305, width=180, height=40)
    button_agencies.place(x=65,y=355, width=180, height= 40)
    button_settings.place(x=65, y=405, width=180, height=40)

# --- Admin Panel --- #
admin_frame = tk.Frame(main_frame, bg='#F1F1F1')

# Main content area
label_admin_welcome = tk.Label(admin_frame, text="", font=("Poppins", 24, "bold"), bg='#F1F1F1')
label_admin_welcome.pack(pady=20)

# Add an admin image label (for the background image)
admin_image_label = tk.Label(admin_frame)
admin_image_label.pack(fill=tk.BOTH, expand=True)

# Create buttons for the admin panel (over the image)
button_statistics = tk.Button(admin_frame, text="Today's Statistics", font="Poppins", command=lambda: print("Statistics"))
button_notifications = tk.Button(admin_frame, text="Notifications", font="Poppins", command=lambda: print("Notifications"))
button_feedback = tk.Button(admin_frame, text="Customer Feedback", font="Poppins", command=lambda: print("Feedback"))
button_car_availability = tk.Button(admin_frame, text="Car Availability", font="Poppins", command=lambda: print("Car Availability"))
button_agencies = tk.Button(admin_frame, text="Agencies", font="Poppins", command=lambda: print("Agencies"))
button_settings = tk.Button(admin_frame, text="Settings", font="Poppins", command=lambda: print("Settings"))

# Logout button (optionally place it later)
button_logout_admin = tk.Button(admin_frame, text="Log out", font="Poppins",
                                command= logout(),
                                bg="#1572D3")
button_logout_admin.place(x=65, y=680, width=180, height=40)



# Start the main event loop
root.mainloop()
