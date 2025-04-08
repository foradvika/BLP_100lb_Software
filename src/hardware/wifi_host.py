import socket
from .serial_com import BT

class Wifi_Host:
    def __init__(self, port):
        try:
            BT.connect_to_esp32()
        except Exception as e:
            print(f"❌ Error: {e}")

    def send_command(self, d):
        '''
        telemetry packet:
        [heartbeat][data layer][aborts][status data]
        '''
        # form packet
        sent = self.connection.sendall(d)
        System_Health.py_stats["wifi message tx"] = 'good'

        if (sent == 0):
            System_Health.py_stats["wifi message tx"] = 'bad'
            raise RuntimeError("socket connection broken at sent")
        return 0

    def recieve_data(self):
        '''
        telemetry packet:
        [heartbeat][data layer][status data]
        '''
        packet_size = 1024
        self.data = self.connection.recv(packet_size)
        print(type(self.data))

        if (self.data == ''):
            System_Health.py_stats["wifi message rx"] = 'bad'
            raise RuntimeError("did not recieve packet")
        else:
            System_Health.py_stats["wifi message rx"] = 'good'

        return self.data 