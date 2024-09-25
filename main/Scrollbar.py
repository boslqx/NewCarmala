import tkinter as tk
from tkinter import ttk

# Step 2: Create the Tkinter Window
root = tk.Tk()
root.title("Scrollable Grid Example")
root.geometry("720x250")

# Step 3: Create a Frame for Grid Layout
frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

# Step 4: Create a Canvas and Scrollbar
canvas = tk.Canvas(frame)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Step 5: Create a Frame for Scrollable Content
content_frame = ttk.Frame(canvas)

# Step 6: Configure the Canvas and Scrollable Content Frame
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Step 7: Add Widgets to the Content Frame
# Example widgets (replace with your own)
label = ttk.Label(content_frame, text="Scrollable Content")
label.grid(row=0, column=0, pady=10)

for i in range(1, 21):
   button = ttk.Button(content_frame, text=f"Button {i}")
   button.grid(row=i, column=0, pady=5)

# Step 8: Create Window Resizing Configuration
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Step 9: Pack Widgets onto the Window
canvas.create_window((0, 0), window=content_frame, anchor="nw")
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Step 10: Bind the Canvas to Mousewheel Events
def _on_mousewheel(event):
   canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Step 11: Run the Tkinter Event Loop
root.mainloop()