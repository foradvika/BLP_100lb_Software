import pandas as pd

class test_sequence:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        
    def parse_test(self):
        # Convert the test sequence to a list of commands
        commands = []
        for _, row in self.df.iterrows():
            time = row['Time']
            function = row['Function']
            action = row['Action']
            commands.append([time, function, action])
        return commands
    
    def parse_abort_limit(self):
        # Parse abort limits if they exist in the file
        # For now, return empty list as this functionality isn't fully implemented
        return [] 