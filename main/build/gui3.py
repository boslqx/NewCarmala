
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\OneDrive - student.newinti.edu.my\Carmala\main\build\assets\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1440x4479")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 4479,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1440.0,
    800.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    800.0,
    1440.0,
    1600.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    1600.0,
    1440.0,
    2400.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    2400.0,
    1440.0,
    3240.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    3240.0,
    1440.0,
    4104.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    4104.0,
    1440.0,
    4479.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
