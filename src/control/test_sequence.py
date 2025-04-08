import time

class TestSequence:
    def __init__(self, telemetry):
        self.telemetry = telemetry
        self.sequence = []
        self.current_step = 0
        self.running = False
        
    def add_step(self, action, duration):
        """Add a step to the test sequence"""
        self.sequence.append({
            'action': action,
            'duration': duration
        })
        
    def clear_sequence(self):
        """Clear the test sequence"""
        self.sequence = []
        self.current_step = 0
        
    def start(self):
        """Start the test sequence"""
        if not self.sequence:
            return False
        self.running = True
        self.current_step = 0
        return True
        
    def stop(self):
        """Stop the test sequence"""
        self.running = False
        self.current_step = 0
        
    def step(self):
        """Execute the current step of the sequence"""
        if not self.running or self.current_step >= len(self.sequence):
            return False
            
        step = self.sequence[self.current_step]
        action = step['action']
        duration = step['duration']
        
        # Execute action
        if action == 'open_valve':
            self.telemetry.open_valve(0)
        elif action == 'close_valve':
            self.telemetry.close_valve(0)
        elif action == 'spark_coil':
            self.telemetry.spark_coil()
            
        # Wait for duration
        time.sleep(duration)
        
        self.current_step += 1
        return True 