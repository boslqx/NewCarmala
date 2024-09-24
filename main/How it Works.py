import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Account Login Page")
root.state('zoomed')  # Set window to full screen

# Add a Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)  # Make the notebook fill the entire window

# Create frames for each tab
home_tab = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
sign_in_tab = ttk.Frame(notebook)

# Add the tabs
notebook.add(home_tab, text='Home')  # New Home tab
notebook.add(tab2, text='Become a Renter')
notebook.add(tab4, text='How It Works')
notebook.add(sign_in_tab, text='Sign In')  # Sign In tab


# Insert and load picture
image = Image.open(r"C:\Users\User\OneDrive\Pictures\Screenshots\屏幕截图 2024-09-24 210757.png")
image = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = tk.Label(root, image=image)
image_label.pack(fill='both', expand=True)

# Start the main event loop
root.mainloop()