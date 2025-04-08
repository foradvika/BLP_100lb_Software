# Authors: Advika Govindarajan, Emily Jones, Adam Abid, Alex Garcia

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
# import os
# import socket
import time
from pycode import Telemetry, System_Health, Metrics
from pycode import V1, V2, V3, V4, C, T, CS, A


# from serial_pc import BT
# import subprocess
# import datetime
# import json

# ---------- Fake Telemetry for Simulation Testing ----------
class FakeTelemetry:
    def __init__(self, sys):
        print("FakeTelemetry: Initialized (Simulation Mode).")
        self.counter = 0

    def start_test(self):
        print("FakeTelemetry: Test started.")

    def send_data(self):
        print("FakeTelemetry: Data sent.")

    def abort(self):
        print("FakeTelemetry: Test aborted.")

    def open_valve(self, valve):
        print(f"FakeTelemetry: Valve {valve} opened.")

    def close_valve(self, valve):
        print(f"FakeTelemetry: Valve {valve} closed.")

    def upload_test_sequence(self, file_path):
        print(f"FakeTelemetry: Uploaded test sequence from {file_path}")

    def get_data(self):
        self.counter += 1
        # Cycle thrust between 0 and 200 lbf
        thrust = self.counter % 201
        # Cycle pressure values between 0 and 850
        pt1 = (self.counter * 2) % 851
        pt2 = (self.counter * 3) % 851
        pt3 = (self.counter * 4) % 851
        pt4 = (self.counter * 5) % 851
        pt5 = (self.counter * 6) % 851
        # Return order: [thrust, pt1, pt2, pt3, pt4, pt5]
        return [thrust, pt1, pt2, pt3, pt4, pt5]


# ---------- Main GUI Class ----------
class GUI:
    def __init__(self):
        # Data storage for graphs
        self.thrust_data = []
        self.pt1_data = []
        self.pt2_data = []
        self.pt3_data = []
        self.pt4_data = []
        self.pt5_data = []

        # all_data will hold rows of [thrust, pt1, pt2, pt3, pt4, pt5]
        self.all_data = []

        # Placeholders for plot elements
        self.thrust_fig = self.thrust_ax = self.thrust_canvas = self.thrust_line = None
        self.pt1_fig = self.pt1_ax = self.pt1_canvas = self.pt1_line = None
        self.pt2_fig = self.pt2_ax = self.pt2_canvas = self.pt2_line = None
        self.pt3_fig = self.pt3_ax = self.pt3_canvas = self.pt3_line = None
        self.pt4_fig = self.pt4_ax = self.pt4_canvas = self.pt4_line = None
        self.pt5_fig = self.pt5_ax = self.pt5_canvas = self.pt5_line = None

        self.chart_canvas = None
        self.PT5_label = None
        self.PT4_label = None
        self.PT3_label = None
        self.PT2_label = None
        self.PT1_label = None
        self.thrust_label = None
        self.temp_label = None
        self.banner_label = None
        self.abort_button = None
        self.start_button = None
        self.OV03_button = None
        self.FV03_button = None
        self.FV02_button = None
        self.NV02_button = None
        self.file_input_entry = None
        self.file_input = None
        self.title = None
        self.timer_label = None
        self.warning_label = None
        self.start_time = None
        self.after_id = None  # for cancelling .after() updates

        self.window = tk.Tk()
        self.window.title("BLP GUI")
        self.window.geometry('1000x1000')
        for i in range(5):
            self.window.columnconfigure(i, weight=1, uniform="col")

        self.valve_status = {'NV-02': 0, 'FV-02': 0, 'FV-03': 0, 'OV-03': 0}
        self.widgets()

    def widgets(self):
        # Timer label
        self.timer_label = tk.Label(self.window, text="Elapsed Time: 0 s",
                                    font=("Times New Roman", 15), fg="black")
        self.timer_label.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        # Warning label
        self.warning_label = tk.Label(self.window, text=" ",
                                      font=("Times New Roman", 15), fg="red")
        self.warning_label.grid(row=2, column=4, sticky="e", padx=5, pady=5)

        # Title
        self.title = tk.Label(self.window,
                              text="BLP GUI",
                              font=("Times New Roman", 25),
                              background="light pink",
                              foreground="black")
        self.title.grid(row=0, columnspan=5, sticky="nsew", pady=(40, 5))

        # File Input
        self.file_input = tk.StringVar()
        self.file_input_entry = tk.Button(self.window,
                                          text="Upload File",
                                          foreground="black",
                                          font=("Times New Roman", 20),
                                          command=self.upload_file)
        self.file_input_entry.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # NV02 Button
        self.NV02_button = tk.Button(self.window,
                                     text="NV-02",
                                     foreground="black",
                                     font=("Times New Roman", 20),
                                     command=lambda: self.toggle_valve(V1))
        self.NV02_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # FV02 Button
        self.FV02_button = tk.Button(self.window,
                                     text="FV-02",
                                     foreground="black",
                                     font=("Times New Roman", 20),
                                     command=lambda: self.toggle_valve(V2))
        self.FV02_button.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # FV03 Button
        self.FV03_button = tk.Button(self.window,
                                     text="FV-03",
                                     foreground="black",
                                     font=("Times New Roman", 20),
                                     command=lambda: self.toggle_valve(V3))
        self.FV03_button.grid(row=2, column=2, sticky="ew", padx=5, pady=5)

        # OV03 Button
        self.OV03_button = tk.Button(self.window,
                                     text="OV-03",
                                     foreground="black",
                                     font=("Times New Roman", 20),
                                     command=lambda: self.toggle_valve(V4))
        self.OV03_button.grid(row=2, column=3, sticky="ew", padx=5, pady=5)

        # Start Button
        self.start_button = tk.Button(self.window,
                                      text="START",
                                      background="green",
                                      foreground="black",
                                      font=("Times New Roman", 20),
                                      command=self.start)
        self.start_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Abort Button
        self.abort_button = tk.Button(self.window,
                                      text="ABORT",
                                      background="red",
                                      foreground="black",
                                      font=("Times New Roman", 20),
                                      command=self.abort)
        self.abort_button.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        # Labels for graphs
        self.thrust_label = tk.Label(self.window,
                                     text="Thrust",
                                     background="white",
                                     foreground="black",
                                     font=("Times New Roman", 15))
        self.thrust_label.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

        self.PT1_label = tk.Label(self.window,
                                  text="Pressure Transducer 1(OPD_02)",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT1_label.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)

        self.PT2_label = tk.Label(self.window,
                                  text="Pressure Transducer 2(FPD_02)",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT2_label.grid(row=5, column=4, sticky="nsew", padx=5, pady=5)

        self.PT3_label = tk.Label(self.window,
                                  text="Pressure Transducer 3(EPD_01)",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT3_label.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)

        self.PT4_label = tk.Label(self.window,
                                  text="Pressure Transducer 4",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT4_label.grid(row=7, column=2, sticky="nsew", padx=5, pady=5)

        self.PT5_label = tk.Label(self.window,
                                  text="Pressure Transducer 5",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT5_label.grid(row=7, column=4, sticky="nsew", padx=5, pady=5)

        # Create plots and store references for updates
        self.thrust_fig, self.thrust_ax, self.thrust_canvas, self.thrust_line = \
            self.create_plot(row=6, column=0, xlabel="Time (s)", ylabel="Thrust (lbf)", data=[])
        self.pt1_fig, self.pt1_ax, self.pt1_canvas, self.pt1_line = \
            self.create_plot(row=6, column=2, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])
        self.pt2_fig, self.pt2_ax, self.pt2_canvas, self.pt2_line = \
            self.create_plot(row=6, column=4, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])
        self.pt3_fig, self.pt3_ax, self.pt3_canvas, self.pt3_line = \
            self.create_plot(row=8, column=0, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])
        self.pt4_fig, self.pt4_ax, self.pt4_canvas, self.pt4_line = \
            self.create_plot(row=8, column=2, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])
        self.pt5_fig, self.pt5_ax, self.pt5_canvas, self.pt5_line = \
            self.create_plot(row=8, column=4, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])

    def create_plot(self, row, column, xlabel, ylabel, data):
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.grid(True)
        if data:
            line, = ax.plot(range(len(data)), data)
        else:
            line, = ax.plot([], [])
        fig.tight_layout(pad=3.0)
        fig.subplots_adjust(bottom=0.3, top=0.9)
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=row, column=column, columnspan=2, sticky="nsew", padx=5, pady=5)
        canvas.draw()
        return fig, ax, canvas, line

    def start(self):
        tel.start_test()
        tel.send_data()
        print("Test started")
        self.start_time = time.time()  # record test start time
        self.update_graphs()  # start telemetry update loop
        self.start_button.config(background="green")
        self.abort_button.config(background="light coral")

    def abort(self):
        tel.abort()
        tel.send_data()
        print("Test aborted")

        # Stop the update loop
        if hasattr(self, "after_id") and self.after_id:
            self.window.after_cancel(self.after_id)

        # Save data to CSV
        self.save_data_to_csv()

        # Optionally, show a message
        messagebox.showinfo("Test Data Saved", "All telemetry data has been saved to test_data.csv")

    def upload_file(self):
        def Start_Count():
            self.start()

        def BLP_Abort():
            self.abort()
            self.test_running = False  # Stop the test sequence
            return "Test aborted and data saved"

        def Read_OPD_02():
            if self.pt1_data and self.pt1_data[-1] < 15:
                    return BLP_Abort()
            return "OPD_02 within safe range"

        def Read_FPD_02():
            if self.pt2_data and self.pt2_data[-1] < 15:
                return BLP_Abort()
            return "FPD_02 within safe range"

        def Read_EPD_01():
            if self.pt3_data and self.pt3_data[-1] < 15:
                return BLP_Abort()
            return ("EPD_01 within safe range")

        def FV_02_Close():
            tel.close_valve(V2)
            tel.send_data()
            self.FV02_button.config(bg="red")
            self.valve_status['FV-02'] = 0
            if self.valve_status["FV-02"] == 1:
                return BLP_Abort()
            return ("FV-02 closed")

        def NV_02_Open():
            tel.open_valve(V1)
            tel.send_data()
            self.NV02_button.config(bg="green")
            self.valve_status['NV-02'] = 1
            if self.valve_status["NV-02"] == 0:
                return BLP_Abort()
            return ("NV-02 opened")

        def OV_03_Open():
            tel.open_valve(V4)
            tel.send_data()
            self.OV03_button.config(bg="green")
            self.valve_status['OV-03'] = 1
            if self.valve_status["OV-03"] == 0:
                return BLP_Abort()
            return ("OV-03 opened")

        def FV_03_Open():
            tel.open_valve(V3)
            tel.send_data()
            self.FV03_button.config(bg="green")
            self.valve_status['FV-03'] = 1
            if self.valve_status["FV-03"] == 0:
                return BLP_Abort()
            return ("FV_03 opened")

        def Spark():                             #Spark function needs to be fixed
            tel.set_coil(16.66667)
            tel.send_data()
            while current_time < spark_time:
                tel.spark_coil()
                tel.send_data()

        function_map = {
            'Start_Count': Start_Count,
            'Read_OPD_02': Read_OPD_02,
            'Read_FPD_02': Read_FPD_02,
            'Read_EPD_01': Read_EPD_01,
            'FV_02': FV_02_Close,
            'NV_02': NV_02_Open,
            'OV_03': OV_03_Open,
            'Ov_03': OV_03_Open,  # Add case-insensitive variant
            'FV_03': FV_03_Open,
            'BLP_Abort': BLP_Abort,
            'Spark': Spark
        }

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            print(f"Selected file: {file_path}")
            try:
                # Read and sort the test sequence
                df = pd.read_csv(file_path)
                test_sequence = list(zip(df['Time'], df['Function']))
                #test_sequence.sort(key=lambda x: x[0])  # Sort by time
                print(test_sequence)

                # Initialize test state
                self.test_running = True
                self.test_start_time = time.time()
                self.current_step = 0

                def execute_test_step():
                    if not self.test_running or self.current_step >= len(test_sequence):
                        return

                    current_time = time.time() - self.test_start_time
                    target_time, function = test_sequence[self.current_step]

                    # If it's time to execute this step
                    if current_time >= target_time:
                        func = function_map.get(function)
                        if func:
                            try:
                                result = func()
                                print(f"Executed {function} at {current_time:.3f}s: {result}")
                            except Exception as e:
                                print(f"Error executing {function}: {e}")
                                self.test_running = False

                        self.current_step += 1

                    # Schedule next check
                    if self.test_running:
                        self.window.after(10, execute_test_step)  # Check every 10ms

                # Start the test sequence
                execute_test_step()

            except Exception as e:
                print(f"Error loading file: {e}")
                self.test_running = False

    def toggle_valve(self, name):
        if name == V1 and self.valve_status['NV-02'] == 0:
            tel.open_valve(V1)
            tel.send_data()
            self.NV02_button.configure(background="green")
            self.valve_status['NV-02'] = 1
            print("NV-02 opened")
        elif name == V2 and self.valve_status['FV-02'] == 0:
            tel.open_valve(V2)
            tel.send_data()
            self.FV02_button.config(bg="green")
            self.valve_status['FV-02'] = 1
            print("FV-02 opened")
        elif name == V3 and self.valve_status['FV-03'] == 0:
            tel.open_valve(V3)
            tel.send_data()
            self.FV03_button.config(bg="green")
            self.valve_status['FV-03'] = 1
            print("FV-03 opened")
        elif name == V4 and self.valve_status['OV-03'] == 0:
            tel.open_valve(V4)
            tel.send_data()
            self.OV03_button.config(bg="green")
            self.valve_status['OV-03'] = 1
            print("OV-03 opened")
        elif name == V1 and self.valve_status['NV-02'] == 1:
            tel.close_valve(V1)
            tel.send_data()
            self.NV02_button.config(bg="red")
            self.valve_status['NV-02'] = 0
            print("NV-02 closed")
        elif name == V2 and self.valve_status['FV-02'] == 1:
            tel.close_valve(V2)
            tel.send_data()
            self.FV02_button.config(bg="red")
            self.valve_status['FV-02'] = 0
            print("FV-02 closed")
        elif name == V3 and self.valve_status['FV-03'] == 1:
            tel.close_valve(V3)
            tel.send_data()
            self.FV03_button.config(bg="red")
            self.valve_status['FV-03'] = 0
            print("FV-03 closed")
        elif name == V4 and self.valve_status['OV-03'] == 1:
            tel.close_valve(V4)
            tel.send_data()
            self.OV03_button.config(bg="red")
            self.valve_status['OV-03'] = 0
            print("OV-03 closed")
        else:
            print("Error toggling valve")

    def update_graphs(self):
        new_data = tel.get_data()
        if new_data and len(new_data) >= 6:
            # Keep a full record
            self.all_data.append(new_data[:6])

            # Update data arrays
            self.pt1_data.append(new_data[0])
            self.pt2_data.append(new_data[1])
            self.pt3_data.append(new_data[2])
            self.pt4_data.append(new_data[3])
            self.pt5_data.append(new_data[4])
            self.thrust_data.append(new_data[5])

            # Update plots
            self.pt1_line.set_data(range(len(self.pt1_data)), self.pt1_data)
            self.pt1_ax.relim()
            self.pt1_ax.autoscale_view()
            self.pt1_canvas.draw()

            self.pt2_line.set_data(range(len(self.pt2_data)), self.pt2_data)
            self.pt2_ax.relim()
            self.pt2_ax.autoscale_view()
            self.pt2_canvas.draw()

            self.pt3_line.set_data(range(len(self.pt3_data)), self.pt3_data)
            self.pt3_ax.relim()
            self.pt3_ax.autoscale_view()
            self.pt3_canvas.draw()

            self.pt4_line.set_data(range(len(self.pt4_data)), self.pt4_data)
            self.pt4_ax.relim()
            self.pt4_ax.autoscale_view()
            self.pt4_canvas.draw()

            self.pt5_line.set_data(range(len(self.pt5_data)), self.pt5_data)
            self.pt5_ax.relim()
            self.pt5_ax.autoscale_view()
            self.pt5_canvas.draw()

            self.thrust_line.set_data(range(len(self.thrust_data)), self.thrust_data)
            self.thrust_ax.relim()
            self.thrust_ax.autoscale_view()
            self.thrust_canvas.draw()

            # Update timer - use the test start time for accuracy
            if hasattr(self, 'test_start_time'):
                elapsed = time.time() - self.test_start_time
                self.timer_label.config(text=f"Elapsed Time: {elapsed:.1f} s")
            elif hasattr(self, 'start_time'):
                elapsed = time.time() - self.start_time
                self.timer_label.config(text=f"Elapsed Time: {elapsed:.1f} s")

            # Optional warnings
            warning_messages = []
            if self.pt1_data and self.pt1_data[-1] > 350:  # Called "EPD_01" in original code
                warning_messages.append("Almost too high EPD_01!")
            if self.pt1_data and self.pt1_data[-1] < 150:
                warning_messages.append("Almost too low EPD_01!")
            if self.pt2_data and self.pt2_data[-1] > 530:
                warning_messages.append("Almost too high FPD_01!")
            if self.pt3_data and self.pt3_data[-1] > 825:
                warning_messages.append("Almost too high OPD_01!")

            self.warning_label.config(text="\n".join(warning_messages))

        # Schedule the next update
        self.after_id = self.window.after(1000, self.update_graphs)

    def save_data_to_csv(self):
        # Create a dictionary to collect time:value pairs for each sensor.
        sensors = {"PT1": [], "PT2": [], "PT3": [], "PT4": [], "PT5": [], "THRUST": []}
        for row in self.all_data:
            # row[0] is the time offset; row[1] is PT1, row[2] is PT2, etc.
            t = row[0]
            sensors["PT1"].append(f"{t}:{row[0]}")
            sensors["PT2"].append(f"{t}:{row[1]}")
            sensors["PT3"].append(f"{t}:{row[2]}")
            sensors["PT4"].append(f"{t}:{row[3]}")
            sensors["PT5"].append(f"{t}:{row[4]}")
            sensors["THRUST"].append(f"{t}:{row[5]}")

        # For each sensor, join the time:value pairs into one string.
        data = []
        for sensor, pairs in sensors.items():
            data.append([sensor, ", ".join(pairs)])

        # Create a DataFrame with two columns: one for the sensor and one for its data.
        df = pd.DataFrame(data, columns=["Sensor", "Time:Value Pairs"])

        # Save the DataFrame to a CSV file.
        csv_filename = "test_data.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}.")


if __name__ == "__main__":
    sys_health = System_Health()
    SIMULATION = True  # Set to False to use real telemetry
    if SIMULATION:
        tel = FakeTelemetry(sys_health)
    else:
        tel = Telemetry(sys_health)
    window = GUI()
    window.window.mainloop()