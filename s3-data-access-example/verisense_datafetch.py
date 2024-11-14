from PIL import Image, ImageTk
import time
from tkinter.font import Font
from pathlib import Path
import tkinter as tk
from download_data_demo import download_data
from tkcalendar import DateEntry
from tkinter import ttk
import threading
"""
CONFIDENTIAL
__________________
2023 Verisense Health Inc.
All Rights Reserved.
NOTICE:  All information contained herein is, and remains
the property of Verisense Health Incorporated and its suppliers,
if any.  The intellectual and technical concepts contained
herein are proprietary to Verisense Health Incorporated
and its suppliers and may be covered by U.S. and Foreign Patents,
patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material
is strictly forbidden unless prior written permission is obtained
from Verisense Health Incorporated.
Authors: Lucas Selig <lselig@verisense.net>
"""


class VerisenseDatafetch:
    def __init__(self, root):
        self.root = root
        self.root.title("Verisense DataFetch")

        # PARTICIPANT Input
        self.part_id_label = ttk.Label(config_frame, text='Participant ID:', font = medium_font)
        self.part_id_label.grid(row = 0, column = 0,  padx = 5, pady = 5)

        participant_default_text = tk.StringVar(value="PL01")
        self.participant_entry = tk.Entry(config_frame, textvariable = participant_default_text)
        self.participant_entry.grid(row = 1, column = 0,  padx = 5, pady = 5)

        # DEVICE_MAC_ID Input
        self.device_id_label = ttk.Label(config_frame, text='Device ID:', font = medium_font)
        self.device_id_label.grid(row = 0, column = 1,  padx = 5, pady = 5)

        device_mac_id_default_text = tk.StringVar(value="04020205FDCC")
        self.device_mac_id_entry = tk.Entry(config_frame, textvariable = device_mac_id_default_text)
        self.device_mac_id_entry.grid(row = 1, column = 1,  padx = 5, pady = 5)

        # Data Selectors

        self.data_start_label = ttk.Label(config_frame, text='Data Begin: ', font = medium_font)
        self.data_start_label.grid(row = 2, column = 0,  padx = 5, pady = 5)
        self.data_end_label = ttk.Label(config_frame, text='Data End: ', font = medium_font)
        self.data_end_label.grid(row = 2, column = 1,  padx = 5, pady = 5)

        self.data_start_entry = DateEntry(config_frame, year = 2024)
        self.data_start_entry.grid(row = 3, column = 0,  padx = 5, pady = 5)
        self.data_end_entry = DateEntry(config_frame, year = 2024)
        self.data_end_entry.grid(row = 3, column = 1,  padx = 5, pady = 5)

        # Output Folder
        self.data_output_folder_label = ttk.Label(config_frame, text='Data Output Folder: ', font = medium_font)
        self.data_output_folder_label.grid(row = 4, column = 0,  padx = 5, pady = 5)

        output_folder_default_text = tk.StringVar(value="/Users/lselig/Desktop/VerisenseData")
        self.output_folder_entry = tk.Entry(config_frame, textvariable=output_folder_default_text)
        self.output_folder_entry.grid(row = 5, column = 0,  padx = 5, pady = 5)

        self.raw_signal_checkbox_states = [tk.IntVar() for _ in range(6)]

        def create_checkbox(text, row, column, frame, states):
            checkbox = tk.Checkbutton(frame, text=text, var=states[row * 2 + column], font = medium_font)
            checkbox.grid(row=row, column=column, padx=10, pady=10)

        def create_checkbox_1d(text, row, column, frame, states):
            checkbox = tk.Checkbutton(frame, text=text, var=states[row], font = medium_font)
            checkbox.grid(row=row, column=column, padx=10, pady=10)

        # Create a 3x2 grid of checkboxes
        self.raw_signal_checkbox_texts = ["Acceleration", "Green PPG", "Red PPG",
                          "Temperature", "Heart Rate", "Blood Oxygen"]
        self.RAW_SIGNALS = ["Accel", "GreenPPG", "RedPPG", "Temperature", "SingleHeartRate", "BloodOxygenLevel"]
        # self.DERIVED_SIGNALS =
        for i in range(3):
            for j in range(2):
                create_checkbox(self.raw_signal_checkbox_texts[i * 2 + j], i, j, raw_signal_frame, self.raw_signal_checkbox_states)


        # self.derived_signal_checkbox_texts = ["GGIR Activity Metrics", "PPG Signal Quality Index", "Non-Wear Metrics"]
        # self.derived_signal_checkbox_states = [tk.IntVar() for _ in range(3)]
        # for i in range(3):
        #     create_checkbox_1d(self.derived_signal_checkbox_texts[i], i, 0, derived_signal_frame, self.derived_signal_checkbox_states)




        # Submit Button
        self.submit_button = ttk.Button(root, style = "TButton",  text='Start Download', command=self.button_click, width = 40)
        self.submit_button.grid(row=2, column=1)
        self.progress = ttk.Progressbar(root, length = 400, orient='horizontal', mode='determinate')

    def start_download(self, callback):
        # self.submit_button.config(text = "Downloading..")
        # self.progress.grid(row=2, column=1)
        # self.progress.start(10)
        participant = self.participant_entry.get()
        device_mac_id = self.device_mac_id_entry.get()
        output_folder = self.output_folder_entry.get()
        data_start = self.data_start_entry.get()
        data_end = self.data_end_entry.get()

        selected_raw_signals = dict(zip(self.RAW_SIGNALS, [x.get() for x in self.raw_signal_checkbox_states]))
        # selected_raw_signals = dict(zip(self.SIGNALS, [x.get() for x in self.raw_signal_checkbox_states]))

        # Assuming 'main_download_function' takes two arguments: PARTICIPANT and DEVICE_MAC_ID
        download_data(participant, device_mac_id, output_folder, data_start, data_end, selected_raw_signals)
        self.root.after(0, callback)
    def start_progress(self):
        # self.progress.start(10)
        # self.submit_button.pack_forget()
        pass
    def finish_download(self):
        self.progress.stop()
        self.progress.grid_remove()
        time.sleep(3)
        self.submit_button.grid(row=2, column=1)
        self.submit_button.config(text = "Completed")
        self.root.destroy()

    def button_click(self):
        self.submit_button.grid_remove()
        self.progress.grid(row=2, column=1)
        self.start_progress()
        self.progress.start(10)
        main_download = threading.Thread(target=self.start_download, args = (self.finish_download,))
        main_download.start()

def center_screen(root):
    # Set the window size
    window_width = 800
    window_height = 500

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate x and y coordinates for the Tk root window
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)

    # Set the window's position
    root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))



if __name__ == "__main__":

    root = tk.Tk()
    big_frame = ttk.Frame(root)
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")

    style = ttk.Style(root)
    image_path = Path.cwd() / 'assets' / 'gradient_with_small_logo.png'
    background_image = Image.open(image_path)
    background_photo = ImageTk.PhotoImage(background_image)

    # Set the background label to hold the image
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Define a larger font
    large_font = Font(family="Helvetica", size=20, weight="bold")
    medium_font = Font(family="Helvetica", size=14, weight="bold")
    medium_font_italic = Font(family="Helvetica", size=14, weight="bold", slant="italic")
    style.configure('TButton', font=medium_font_italic)
    style.configure('TFrame', borderwidth=2, relief='groove')

    center_screen(root)



    # Add labels to the frames
    config_frame_label = ttk.Label(root, text="Config", font = large_font)
    config_frame_label.grid(row=0, column=0, padx=5, pady=(5, 0))

    raw_signal_label = ttk.Label(root, text="Select Raw Signals", font = large_font)
    raw_signal_label.grid(row=0, column=1, padx=5, pady=(5, 0))

    # derived_signal_label = ttk.Label(root, text="Select Derived Signals", font = large_font)
    # derived_signal_label.grid(row=0, column=2, padx=5, pady=(5, 0))

    # Set up the three frames
    config_frame = ttk.Frame(root, style="TFrame")
    config_frame.grid(row=1, column=0, padx=20, pady=20)

    raw_signal_frame = ttk.Frame(root, style="TFrame")
    raw_signal_frame.grid(row=1, column=1, padx=20, pady=20)

    derived_signal_frame = ttk.Frame(root, style="TFrame")
    derived_signal_frame.grid(row=1, column=2, padx=20, pady=20)

    app = VerisenseDatafetch(root)
    root.mainloop()