import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Pack Example")

# Create buttons
button1 = tk.Button(root, text="Button 1")
button2 = tk.Button(root, text="Button 2")
button3 = tk.Button(root, text="Button 3")

# Pack buttons
button1.pack(side=tk.TOP, fill=tk.X)   # Pack at the top, fill horizontally
button2.pack(side=tk.LEFT, fill=tk.Y)  # Pack on the left, fill vertically
button3.pack(side=tk.BOTTOM, expand=True)  # Pack at the bottom, expand to fill space

# Run the application
root.mainloop()
