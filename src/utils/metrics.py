class Metrics:
    def __init__(self):
        self.data = {}
        
    def update_metrics(self, key, value):
        self.data[key] = value
        
    def get_metrics(self):
        return self.data 