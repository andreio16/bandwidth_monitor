#region imports
import requests
import matplotlib
import tkinter as tk
import subprocess, os, signal
import matplotlib.animation as animation

from tkinter import *
from time import sleep
from datetime import date, datetime
from Common import network_tracker
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


matplotlib.use("TkAgg")
style.use("ggplot")

#endregion

#region Global variables
root = Tk()
label_frame = LabelFrame(root)
btn_show_diagram = Button(label_frame)
btn_start_server = Button(label_frame)
btn_reset_server = Button(label_frame)
figure = Figure(figsize=(6.5, 3), dpi=100)
chart = figure.add_subplot(111)

server_process = None
BASE = "http://127.0.0.1:5000/"
#endregion

#region Functions

# UI design func
def init_main_window():
    root.title("Demo App")
    root.geometry('800x300')
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
    btn_start_server.config(command=btn_start_server_on_click)

def init_btn_reset_server():
    btn_reset_server.config(text="Reset Server")
    btn_reset_server.grid(column=0, row=1, padx=5, pady=10)
    btn_reset_server.config(bg="azure", fg="black", borderwidth=2, relief=tk.RAISED, font="Terminal 8")
    btn_reset_server.config(command=btn_reset_server_on_click, state="disable")

def init_btn_draw_diagram():
    btn_show_diagram.config(text="Draw")
    btn_show_diagram.grid(column=1, row=0, padx=5, pady=10)
    btn_show_diagram.config(command=btn_draw_diagram_on_click)
    btn_show_diagram.config(bg="azure", fg="black", borderwidth=2, relief=tk.RAISED, font="Terminal 8")

def initialize_gui_design():
    # root window 
    init_main_window()

    # controls
    init_buttons_group()

    # diagram-chart
    init_chart_diagram()

def init_chart_diagram(x_list=[], y_list=[]):
    # background computing / we need to bring it up to tkinter interface
    chart.clear()
    chart.plot(x_list, y_list)
    chart.xaxis.set_ticks(range(0, len(x_list), 2))

    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=0, rowspan=2)

    toolbar_frame = Frame(root)
    toolbar_frame.grid(column=1, row=0, sticky=N)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()


# UI action func

def btn_draw_diagram_on_click():
    x_time_axis_list, y_values_axis_list = extract_data_from_db()
    init_chart_diagram(x_time_axis_list, y_values_axis_list)

def btn_start_server_on_click():
    global server_process
    server_process = subprocess.Popen(["python", "./Common/database_api.py"])    
    btn_start_server.config(state="disable")
    btn_reset_server.config(state="normal")

def btn_reset_server_on_click():   
    init_chart_diagram()
    terminate_process(server_process)
    btn_start_server.config(state="normal")
    btn_reset_server.config(state="disable")


# Database operations func
def extract_data_from_db():
    time = []
    resource = []
    lenght = get_nr_of_tuples_from_db()

    for i in range(lenght):
        response = requests.get(BASE + "resource/" + str(i))

        # extract only the time hms from the datetime
        temp_time = response.json()['timestamp'][12:]
        temp_resource = response.json()['mega_bits_per_second']

        time.append(temp_time)
        resource.append(temp_resource)
    return time, resource

def del_all_tuples_from_db():
    lenght = get_nr_of_tuples_from_db()
    
    for i in range(lenght):
        response = requests.delete(BASE + "resource/" + str(i))

def get_nr_of_tuples_from_db():
    response = requests.get(BASE + "nr_resources")
    return response.json()['nr_resources']


# Process win func
def terminate_process(process):
    from subprocess import call
    if process.poll() is None:
        call('taskkill /F /T /PID ' + str(process.pid))

#endregion



#region Main func
if __name__ == "__main__":
    initialize_gui_design()
    root.mainloop()

#endregion