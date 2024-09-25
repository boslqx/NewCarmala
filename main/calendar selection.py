from tkinter import *
from tkcalendar import *

root = Tk()
root.geometry('1280x780')

# get the selected date when user close calendar
def pick_date(event):
    global cal, date_window

    date_window = Toplevel()
    date_window.grab_set()
    date_window.title('Choose date of birth')
    date_window.geometry('220x220+590+3770')
    cal = Calendar(date_window, selectmode="day", date_pattern="mm/dd/y")
    cal.place(x=0,y=0)

    submit_btn = Button(date_window, text = "submit", command = grab_date)
    submit_btn.place(x=80, y=190)

def grab_date():
    dob_entry.delete(0,END)
    dob_entry.insert(0, cal.get_date())
    date_window.destroy()

# date of birth label
dob_label = Label(root, text = "Date of birth: ",bg="black", fg="white")
dob_label.place(x=40, y=160)

dob_entry = Entry(root, highlightthickness=0, relief=FLAT, bg="white")
dob_entry.place(x=160, y=160, width=255)
dob_entry.insert(0, "dd/mm/yyyy")
dob_entry.bind("<1>", pick_date)

root.mainloop()

