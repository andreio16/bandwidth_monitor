from tkinter import *
from Common import network_tracker

# GLOBAL VARIABLES
root = Tk()
root.title("Demo App")
root.geometry('150x30')


# FUNCTIONS
def dummy_main():
    frame = Frame(root)
    frame.pack()

    label = Label(frame, text="Hi All!")
    label.pack()

    button = Button(frame, text="Close me!", command=root.destroy)
    button.pack(side='top')


# def flash_main():
#     global old_value, mb_rounded
#     new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
#     meg_bytes = new_value - old_value
#     meg_bytes  = meg_bytes/1024.0/1024.0*8

#     if meg_bytes:
#         mb_rounded = round(meg_bytes, 3)
#         flash_buttons()

#     old_value = new_value
#     root.after(20, flash_main) 

# root.after(10, flash_main)


root.mainloop()
