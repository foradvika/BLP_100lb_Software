"""
file: main_window.py
author: Alex Garcia
course: Baylor Aero
assignment: BLP GUI

date modified: 2024-04-08
- Added log file functionality with timestamped files
- Improved GUI layout and responsiveness
- Added terminal output display in GUI

This file implements the main GUI window for the BLP control system. It provides
real-time visualization of sensor data, valve control buttons, and test sequence
execution capabilities. The window includes plots for thrust and pressure readings,
along with controls for file upload, test start/abort, and valve operations.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import time
from src.control.telemetry import Telemetry, V1, V2, V3, V4, C, T, CS, A
import os
from datetime import datetime

class MainWindow:
    """
    MainWindow
    
    This class implements the main GUI window for the BLP control system.
    It handles all user interactions, real-time data visualization, and
    test sequence execution.
    
    Attributes:
        thrust_data: List storing thrust sensor readings
        pt1_data through pt5_data: Lists storing pressure transducer readings
        time_data: List storing time points for plotting
        test_file_path: Path to the current test sequence file
        test_running: Boolean indicating if a test is currently running
        valve_buttons: Dictionary storing references to valve control buttons
        log_file_path: Path to the current session's log file
    """
    def __init__(self):
        # Data storage for graphs
        self.thrust_data = []
        self.pt1_data = []
        self.pt2_data = []
        self.pt3_data = []
        self.pt4_data = []
        self.pt5_data = []
        self.time_data = []
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create new log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file_path = os.path.join(logs_dir, f'test_log_{timestamp}.txt')
        self.log_file = open(self.log_file_path, 'w')
        print(f"Log file created: {self.log_file_path}")
        
        self.window = tk.Tk()
        self.window.title("BLP GUI")
        self.window.geometry('1200x800')  # Wider window to accommodate log
        
        # Create main container frame
        self.main_container = tk.Frame(self.window)
        self.main_container.pack(fill="both", expand=True)
        
        # Create left frame for controls and plots
        self.left_frame = tk.Frame(self.main_container)
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        # Create right frame for log
        self.right_frame = tk.Frame(self.main_container)
        self.right_frame.pack(side="right", fill="y", padx=5)
        
        # Create log text widget
        self.log_text = tk.Text(self.right_frame, width=40, height=45, font=("Courier", 9))
        self.log_scroll = ttk.Scrollbar(self.right_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scroll.set)
        
        # Pack log widgets
        self.log_text.pack(side="left", fill="y")
        self.log_scroll.pack(side="right", fill="y")
        
        # Create scrollable frame for plots and controls
        self.canvas = tk.Canvas(self.left_frame)
        v_scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.left_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Configure grid
        for i in range(3):
            self.scrollable_frame.columnconfigure(i, weight=1)
        
        # Initialize control systems
        self.telemetry = Telemetry(self)
        
        # Test sequence file path
        self.test_file_path = None
        self.test_running = False
        self.start_time = None
        
        # Store valve buttons for easy access
        self.valve_buttons = {}
        
        # Create GUI elements
        self.create_widgets()
        
        # Redirect stdout to both log file and text widget
        import sys
        self.stdout = sys.stdout
        sys.stdout = self
        
    def write(self, text):
        """Write function for stdout redirection"""
        self.stdout.write(text)  # Write to actual stdout
        self.log_file.write(text)  # Write to log file
        self.log_file.flush()  # Ensure it's written immediately
        self.log_text.insert("end", text)
        self.log_text.see("end")  # Auto-scroll to bottom
        self.window.update_idletasks()
        
    def flush(self):
        """Flush function for stdout redirection"""
        self.stdout.flush()
        self.log_file.flush()
        
    def __del__(self):
        """Restore stdout and close log file when the window is closed"""
        import sys
        sys.stdout = self.stdout
        if hasattr(self, 'log_file'):
            self.log_file.close()
            print(f"Log file closed: {self.log_file_path}")
        
    def create_widgets(self):
        # Title
        self.title = tk.Label(self.scrollable_frame,
                            text="BLP GUI",
                            font=("Times New Roman", 16),
                            background="light pink",
                            foreground="black")
        self.title.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=2)  # Reduced columnspan

        # Control Frame - Center aligned with fixed width
        control_frame = tk.Frame(self.scrollable_frame)
        control_frame.grid(row=1, column=0, columnspan=3, sticky="n", padx=2, pady=2)
        
        # File Upload Button
        self.file_button = tk.Button(control_frame,
                                   text="Upload File",
                                   foreground="black",
                                   font=("Times New Roman", 10),
                                   width=10)
        self.file_button.pack(side=tk.LEFT, padx=5)
        self.file_button.config(command=self.upload_file)

        # Start Button
        self.start_button = tk.Button(control_frame,
                                    text="START",
                                    background="green",
                                    foreground="white",
                                    font=("Times New Roman", 10),
                                    width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.start_button.config(command=self.start)

        # Abort Button
        self.abort_button = tk.Button(control_frame,
                                    text="ABORT",
                                    background="red",
                                    foreground="white",
                                    font=("Times New Roman", 10),
                                    width=10)
        self.abort_button.pack(side=tk.LEFT, padx=5)
        self.abort_button.config(command=self.abort)

        # Timer label
        self.timer_label = tk.Label(control_frame,
                                  text="Elapsed Time: 0 s",
                                  font=("Times New Roman", 10),
                                  fg="black")
        self.timer_label.pack(side=tk.LEFT, padx=5)

        # Valve Frame - Center aligned with fixed width
        valve_frame = tk.Frame(self.scrollable_frame)
        valve_frame.grid(row=2, column=0, columnspan=3, sticky="n", padx=2, pady=2)
        
        # Valve Buttons
        valves = [
            ("NV-02", V1),
            ("FV-02", V2),
            ("FV-03", V3),
            ("OV-03", V4)
        ]
        
        for i, (name, valve_id) in enumerate(valves):
            btn = tk.Button(valve_frame,
                          text=name,
                          foreground="black",
                          font=("Times New Roman", 10),
                          width=8)
            btn.pack(side=tk.LEFT, padx=5)  # Using pack instead of grid
            btn.config(command=lambda v=valve_id: self.toggle_valve(v))
            self.valve_buttons[valve_id] = btn

        # Warning label
        self.warning_label = tk.Label(self.scrollable_frame,
                                    text=" ",
                                    font=("Times New Roman", 10),
                                    fg="red")
        self.warning_label.grid(row=3, column=0, columnspan=3, sticky="n", pady=2)

        # Create plots frame to contain all plots
        plots_frame = tk.Frame(self.scrollable_frame)
        plots_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")
        
        # Configure plot frame grid
        for i in range(3):  # 3 columns for plots
            plots_frame.columnconfigure(i, weight=1)
        
        # Create plots
        self.create_plots(plots_frame)
        
        # Start graph updates
        self.update_graphs()
        
    def create_plots(self, plots_frame):
        # Create figure for thrust with smaller size
        self.thrust_fig = Figure(figsize=(4, 2.5), dpi=100)
        self.thrust_ax = self.thrust_fig.add_subplot(111)
        self.thrust_ax.set_xlabel("Time (s)", fontsize=8)
        self.thrust_ax.set_ylabel("Thrust (lbf)", fontsize=8)
        self.thrust_ax.grid(True)
        self.thrust_ax.set_title("Thrust", pad=5, fontsize=10)
        self.thrust_fig.tight_layout()
        self.thrust_canvas = FigureCanvasTkAgg(self.thrust_fig, master=plots_frame)
        self.thrust_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        # Create figures for pressure transducers
        self.pt_figs = []
        self.pt_axes = []
        self.pt_canvases = []
        
        # Labels for the plots
        self.plot_labels = [
            "PT1 (OPD_02)",
            "PT2 (FPD_02)",
            "PT3 (EPD_01)",
            "PT4",
            "PT5"
        ]
        
        # Arrange plots in a more compact grid
        plot_positions = [
            (0, 1), (0, 2),  # First row
            (1, 0), (1, 1), (1, 2)  # Second row
        ]
        
        for i, (row, col) in enumerate(plot_positions):
            fig = Figure(figsize=(4, 2.5), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_xlabel("Time (s)", fontsize=8)
            ax.set_ylabel("Pressure (PSI)", fontsize=8)
            ax.set_title(self.plot_labels[i], pad=5, fontsize=10)
            ax.grid(True)
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=plots_frame)
            canvas.get_tk_widget().grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            
            self.pt_figs.append(fig)
            self.pt_axes.append(ax)
            self.pt_canvases.append(canvas)
        
    def update_graphs(self):
        if self.test_running:
            current_time = time.time() - self.start_time
            self.time_data.append(current_time)
            
            # Get new data from telemetry
            data = self.telemetry.get_data()
            if data:
                thrust, pt1, pt2, pt3, pt4, pt5 = data
                
                # Update data lists
                self.thrust_data.append(thrust)
                self.pt1_data.append(pt1)
                self.pt2_data.append(pt2)
                self.pt3_data.append(pt3)
                self.pt4_data.append(pt4)
                self.pt5_data.append(pt5)
                
                # Update thrust plot
                self.thrust_ax.clear()
                self.thrust_ax.plot(self.time_data, self.thrust_data, 'b-')
                self.thrust_ax.set_xlabel("Time (s)", fontsize=8)
                self.thrust_ax.set_ylabel("Thrust (lbf)", fontsize=8)
                self.thrust_ax.grid(True)
                self.thrust_ax.set_title("Thrust", pad=5, fontsize=10)
                self.thrust_fig.tight_layout()
                self.thrust_canvas.draw()
                
                # Update pressure plots
                pt_data = [self.pt1_data, self.pt2_data, self.pt3_data, 
                          self.pt4_data, self.pt5_data]
                
                for i, (ax, canvas, data, fig) in enumerate(zip(self.pt_axes, 
                                                              self.pt_canvases, 
                                                              pt_data,
                                                              self.pt_figs)):
                    ax.clear()
                    ax.plot(self.time_data, data, 'r-')
                    ax.set_xlabel("Time (s)", fontsize=8)
                    ax.set_ylabel("Pressure (PSI)", fontsize=8)
                    ax.grid(True)
                    ax.set_title(self.plot_labels[i], pad=5, fontsize=10)
                    fig.tight_layout()
                    canvas.draw()
            
            # Update timer
            self.timer_label.config(text=f"Elapsed Time: {current_time:.1f} s")
            
        self.window.after(100, self.update_graphs)  # Update every 100ms
        
    def upload_file(self):
        """Handle test sequence file upload"""
        filetypes = [
            ('CSV files', '*.csv'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Test Sequence File",
            filetypes=filetypes
        )
        
        if filename:
            self.test_file_path = filename
            self.telemetry.upload_test_sequence(filename)
            self.warning_label.config(text="Test sequence loaded")
            
    def start(self):
        if not self.test_file_path:
            messagebox.showerror("Error", "Please upload a test sequence first")
            return
            
        self.test_running = True
        self.start_time = time.time()
        self.telemetry.start_test()
        self.start_button.config(state="disabled")
        self.warning_label.config(text="Test Running")
        
    def abort(self):
        self.test_running = False
        self.telemetry.abort()
        self.start_button.config(state="normal")
        self.warning_label.config(text="Test Aborted", fg="red")
        
    def toggle_valve(self, valve_id):
        """Toggle valve state"""
        if valve_id in self.valve_buttons:
            button = self.valve_buttons[valve_id]
            if button.cget("background") != "green":
                self.telemetry.open_valve(valve_id)
                button.config(background="green")
            else:
                self.telemetry.close_valve(valve_id)
                button.config(background="red")
                
    def update_valve_state(self, valve_id, state):
        """Update valve button state from test sequence"""
        if valve_id in self.valve_buttons:
            button = self.valve_buttons[valve_id]
            if state == 'OPEN':
                button.config(background="green")
            elif state == 'CLOSE':
                button.config(background="red")
        
    def run(self):
        self.window.mainloop()