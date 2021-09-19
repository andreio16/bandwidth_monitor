#region imports
import time
import requests
import matplotlib
import tkinter as tk
import subprocess, os, signal
import matplotlib.animation as animation

from tkinter import *
from matplotlib import style
from matplotlib.figure import Figure
from datetime import date, datetime
from Common.network_tracker import NetworkTracker 
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
bandwidth_tracker = NetworkTracker()
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
    btn_start_server.config(bg="DarkSeaGreen1", fg="black", borderwidth=2, relief=tk.RAISED, font="Terminal 8")
    btn_start_server.config(command=btn_start_server_on_click)

def init_btn_reset_server():
    btn_reset_server.config(text="Reset Server")
    btn_reset_server.grid(column=0, row=1, padx=5, pady=10)
    btn_reset_server.config(bg="cornsilk", fg="black", borderwidth=2, relief=tk.RAISED, font="Terminal 8")
    btn_reset_server.config(command=btn_reset_server_on_click, state="disable")

def init_btn_draw_diagram():
    btn_show_diagram.config(text="Draw")
    btn_show_diagram.grid(column=1, row=0, padx=5, pady=10)
    btn_show_diagram.config(command=btn_draw_diagram_on_click)
    btn_show_diagram.config(bg="GhostWhite", fg="black", borderwidth=2, relief=tk.RAISED, font="Terminal 8")

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
    is_server_ok, server_message = check_db_server_status()

    if is_server_ok == False:
        tk.messagebox.showwarning(title='Server status.', message=server_message)
    else:
        x_time_axis_list, y_values_axis_list = extract_data_from_db()
        init_chart_diagram(x_time_axis_list, y_values_axis_list)

def btn_start_server_on_click():
    global server_process
    server_process = subprocess.Popen(["python", "./Common/db_api_server.py"])    
    btn_reset_server.config(state="normal", bg="DarkSeaGreen1")
    btn_start_server.config(state="disable", bg="cornsilk")
    bandwidth_tracker.dispose()
    while True:
        if bandwidth_tracker.traker_started == False:
            break
        # Get the upload/download speed from bit/s to Mbit/s
        time.sleep(5)
        upload_speed = (bandwidth_tracker.get_current_upload_speed() / (2**20))
        download_speed = (bandwidth_tracker.get_current_download_speed() / (2**20))
        total_data_used = round(bandwidth_tracker.get_total_data_used() / (2**20), 3)
        send_tuple_to_db(datetime.now(), total_data_used)

def btn_reset_server_on_click():   
    init_chart_diagram()
    terminate_process(server_process)
    btn_reset_server.config(state="disable", bg="cornsilk")
    btn_start_server.config(state="normal", bg="DarkSeaGreen1")
    if bandwidth_tracker.traker_started:
        bandwidth_tracker.dispose()
    else:
        bandwidth_tracker.activate()


# Database operations func
def extract_data_from_db():
    time = []
    resource = []
    lenght = get_nr_of_tuples_from_db()
    print(lenght)

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

def check_db_server_status():
    is_db_running = True
    message_status = 'Database running...'
    try:
        length = get_nr_of_tuples_from_db()
    except Exception as e:
        message_status = 'Server is down, please perform a restart.'
        is_db_running = False
    return is_db_running, message_status

def get_nr_of_tuples_from_db():
    response = requests.get(BASE + "nr_resources")
    return response.json()['nr_resources']

# def get_next_tuple_index_from_db():
#     if get_nr_of_tuples_from_db() > 0:
#         return get_nr_of_tuples_from_db() + 1
#     else:
#         return 0

def send_tuple_to_db(timestamp, bandwidth_val):
    json_obj = {}
    tuple_idx = get_nr_of_tuples_from_db()
    json_obj['mega_bits_per_second'] = bandwidth_val
    json_obj['timestamp'] = timestamp.strftime("%d %b %Y, %H:%M:%S")
    requests.put(BASE + "resource/" + str(tuple_idx), json_obj)



# Process win func
def terminate_process(process):
    from subprocess import call
    if process.poll() is None:
        call('taskkill /F /T /PID ' + str(process.pid))

#endregion



#region Main func
def Main():
    initialize_gui_design()
    root.mainloop()

if __name__ == "__main__":
    Main()
#endregion