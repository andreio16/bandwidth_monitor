from tkinter import *
from tkinter.ttk import *

root = Tk()
root.title("Demo App")
root.geometry('500x50')

frame = Frame(root)
frame.pack()

label = Label(frame, text="Hi All!")
label.pack()

button = Button(frame, text="Close me!", command=root.destroy)
button.pack(side='top')

root.mainloop()
