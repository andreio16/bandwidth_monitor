#region IMPORTS
import tkinter as tk
import matplotlib
import matplotlib.animation as animation

from tkinter import *
from Common import network_tracker
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


matplotlib.use("TkAgg")
style.use("ggplot")

#endregion

#region GLOBAL VARIABLES
root = Tk()
label_frame = LabelFrame(root)
btn_show_diagram = Button(label_frame)
btn_start_server = Button(label_frame)
btn_reset_server = Button(label_frame)

figure = Figure(figsize=(4.5, 3), dpi=100)
chart = figure.add_subplot(111)

#endregion

#region FUNCTIONS
def initialize_gui_design():
    # root window 
    init_main_window()

    # controls
    init_buttons_group()

    # diagram-chart
    init_chart_diagram()

def init_main_window():
    root.title("Demo App")
    root.geometry('600x300')
    root.resizable(False, False)

def init_buttons_group():
    # label frame 
    label_frame.config(text="Actions Panel")
    label_frame.grid(column=0, row=0, padx=5, pady=100)
    
    # buttons
    init_btn_start_server()
    init_btn_reset_server()
    init_btn_draw_diagram()

def init_btn_start_server():
    btn_start_server.config(text="Start Server")
    btn_start_server.grid(column=0, row=0, padx=5, pady=10)
    btn_start_server.config(bg="azure", fg="black", borderwidth=2, relief=tk.RAISED, font="Terminal 8")

def init_btn_reset_server():
    btn_reset_server.config(text="Reset Server")
    btn_reset_server.grid(column=0, row=1, padx=5, pady=10)
    btn_reset_server.config(bg="azure", fg="black", borderwidth=2, relief=tk.RAISED, font="Terminal 8")

def init_btn_draw_diagram():
    btn_show_diagram.config(text="Draw")
    btn_show_diagram.grid(column=1, row=0, padx=5, pady=10)
    btn_show_diagram.config(bg="azure", fg="black", borderwidth=2, relief=tk.RAISED, font="Terminal 8")

def init_chart_diagram():
    # background computing / we need to bring it up to tkinter interface
    chart.plot([], [])     

    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=0, rowspan=2)

    toolbar_frame = Frame(root)
    toolbar_frame.grid(column=1, row=0, sticky=N)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()

def extract_data_from_db():
    pass

#endregion

initialize_gui_design()
root.mainloop()
