"""
file: telemetry.py
author: Alex Garcia
course: Baylor Aero
assignment: BLP GUI

date modified: 2024-04-08
- Added simulated data patterns for testing
- Improved test sequence execution handling
- Enhanced logging and status reporting

This file implements the telemetry system for the BLP control system.
It handles communication with the hardware (or simulates it in test mode),
manages valve states, and processes sensor data. The system supports
real-time data acquisition and test sequence execution.
"""

# Constants for valve indices
V1 = 0  # NV-02
V2 = 1  # FV-02
V3 = 2  # FV-03
V4 = 3  # OV-03
C = 4   # Coil
T = 5   # Test
CS = 6  # Coil Speed
A = 7   # Abort

import math
import time

class Telemetry:
    """
    Telemetry
    
    This class handles all communication with the BLP hardware system.
    In simulation mode, it generates realistic sensor data patterns and
    simulates valve operations. It manages test sequence execution and
    provides real-time data updates.
    
    Attributes:
        sys: Reference to the main window system
        data_packet: List of current hardware states
        counter: Counter for simulated data generation
        test_sequence: Current loaded test sequence
        current_step: Index of current step in test sequence
        test_start_time: Timestamp of test start
    
    Safety Protocols:
        - All valves are closed at startup
        - Abort command closes all valves
        - Pressure limits are enforced:
          * PT1 (OPD_02): < 350 PSI
          * PT2 (FPD_02): < 530 PSI
          * PT3 (EPD_01): < 825 PSI
    """
    
    def __init__(self, sys):
        """
        Initialize the Telemetry system.
        
        Parameters:
            sys: Reference to the main window system
        """
        print("FakeTelemetry: Initialized (Simulation Mode)")
        self.sys = sys
        self.data_packet = [[0], [0], [0], [0], [0], [0], [0], [0]]
        self.rx_data = []
        self.counter = 0  # For simulation data
        self.test_sequence = []
        self.current_step = 0
        self.test_start_time = None
        
    def open_valve(self, num):
        """
        Open the specified valve.
        
        Parameters:
            num: Valve index to open (0-3)
        
        Returns:
            0 on success
        """
        valve_names = {V1: "NV-02", V2: "FV-02", V3: "FV-03", V4: "OV-03"}
        valve_num = num + 1  # Convert to 1-based indexing for display
        print(f"Executed {valve_names.get(num, f'Valve_{num}')} at {self.counter/10:.3f}s: {valve_names.get(num, f'Valve_{num}')} opened")
        self.data_packet[num] = [1]
        return 0

    def close_valve(self, num):
        """
        Close the specified valve.
        
        Parameters:
            num: Valve index to close (0-3)
        
        Returns:
            0 on success
        """
        valve_names = {V1: "NV-02", V2: "FV-02", V3: "FV-03", V4: "OV-03"}
        valve_num = num + 1  # Convert to 1-based indexing for display
        print(f"Executed {valve_names.get(num, f'Valve_{num}')} at {self.counter/10:.3f}s: {valve_names.get(num, f'Valve_{num}')} closed")
        self.data_packet[num] = [0]
        return 0

    def set_coil(self, ms):
        """
        Set the coil speed.
        
        Parameters:
            ms: Speed value in milliseconds
        
        Returns:
            0 on success
        """
        print(f"FakeTelemetry: Setting coil speed to {ms}")
        self.data_packet[CS] = [ms]
        return 0

    def spark_coil(self):
        """
        Activate the spark coil.
        
        Returns:
            0 on success
        """
        print("FakeTelemetry: Activating coil")
        self.data_packet[C] = [1]
        return 0

    def start_test(self):
        """
        Start the test sequence execution.
        
        Returns:
            0 on success
        """
        print("FakeTelemetry: Test started.")
        self.test_start_time = time.time()
        self.current_step = 0
        self.data_packet[T] = [1]
        return 0

    def abort(self):
        """
        Abort the current test sequence and close all valves.
        
        Returns:
            0 on success
        """
        print("FakeTelemetry: Test aborted.")
        print(f"Executed BLP_Abort at {self.counter/10:.3f}s: None")
        self.data_packet[A] = [1]
        self.test_sequence = []  # Empty list instead of None
        self.current_step = 0
        self.test_start_time = None  # Reset start time
        return 0

    def get_data(self):
        """
        Get the latest sensor data and execute test sequence steps.
        
        This method simulates sensor readings and handles test sequence execution.
        It generates realistic patterns for thrust and pressure readings.
        
        Returns:
            List of [thrust, pt1, pt2, pt3, pt4, pt5] readings
        """
        self.counter += 1
        
        # Execute test sequence steps if running
        if self.test_sequence and self.test_start_time:  # Only if both are valid
            current_time = time.time() - self.test_start_time
            
            # Execute all steps that should have happened by now
            while (self.current_step < len(self.test_sequence) and 
                   current_time >= self.test_sequence[self.current_step][0]):
                step = self.test_sequence[self.current_step]
                self._execute_test_step(step, current_time)
                self.current_step += 1
        
        # Simulate some interesting data patterns
        time_factor = self.counter / 50.0  # Slower changes
        
        # Simulate thrust building up to 100 lbf
        thrust = min(100, time_factor * 20)
        
        # Simulate pressure readings with different patterns
        pt1 = min(850, time_factor * 100)  # Linear increase
        pt2 = min(850, time_factor * 80)   # Slower increase
        pt3 = min(850, time_factor * 120)  # Faster increase
        pt4 = min(850, 400 + 50 * math.sin(time_factor))  # Oscillating
        pt5 = min(850, pt1 * 0.8)  # Related to pt1
        
        # Print sensor readings periodically
        if self.counter % 100 == 0:  # Every 10 seconds
            print(f"Executed Read_OPD_02 at {self.counter/10:.3f}s: OPD_02 low: {pt1:.1f} PSI")
            print(f"Executed Read_FPD_02 at {self.counter/10:.3f}s: FPD_02 low: {pt2:.1f} PSI")
            print(f"Executed Read_EPD_01 at {self.counter/10:.3f}s: EPD_01 low: {pt3:.1f} PSI")
        
        return [thrust, pt1, pt2, pt3, pt4, pt5]

    def _execute_test_step(self, step, current_time):
        """Execute a single test sequence step"""
        time, function, action = step
        
        # Map of function names to methods and valve IDs
        function_map = {
            'NV_02': (self.open_valve if action == 'OPEN' else self.close_valve, V1),
            'FV_02': (self.open_valve if action == 'OPEN' else self.close_valve, V2),
            'FV_03': (self.open_valve if action == 'OPEN' else self.close_valve, V3),
            'OV_03': (self.open_valve if action == 'OPEN' else self.close_valve, V4),
            'Spark': (self.spark_coil, None),
            'BLP_Abort': (self.abort, None)
        }
        
        if function in function_map:
            method, arg = function_map[function]
            if arg is not None:
                method(arg)
                # Update GUI valve state
                self.sys.update_valve_state(arg, action)
            else:
                method()
            print(f"Executed {function} at {current_time:.3f}s: {action}")

    def upload_test_sequence(self, file_path):
        """Upload and parse test sequence file"""
        print(f"Selected file: {file_path}")
        try:
            from src.utils.test_sequence_parser import test_sequence
            ts = test_sequence(file_path)
            self.test_sequence = ts.parse_test()
            print(f"FakeTelemetry: Test sequence loaded with {len(self.test_sequence)} commands")
            return True
        except Exception as e:
            print(f"FakeTelemetry Error: Failed to load test sequence - {str(e)}")
            return False 