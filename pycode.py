'''
Author: Izuka Ikedionwu

Description: python side to interface with pi and front this is the middle man

features:
- streamlined wifi

Created: 6/28/24
'''

# dependencies

# wifi
import socket
import numpy
import json
import struct
import serial
from threading import Timer
import time
#from serial_pc import BT
import uart_code1
from test_sequ_excel import test_sequence

# global variables
V1 = 0
V2 = 1
V3 = 2
V4 = 3
P1 = 4
P2 = 5
P3 = 6
P4 = 7

C = 4
T = 5
CS = 6
A = 7


# ToDo: add anymore numbers for front end
# SERIAL_PORT = "COM7"  # Change this based on your system
# BAUD_RATE = 115200  # Match the baud rate of your ESP32/Arduino
# ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

class System_Health:
    '''
    Shared Data
    '''
    py_stats = {}
    pi_stats = {}
    sys_stats = {}

    #        measurement             default status
    py_stats['init wifi connection'] = 'null'
    py_stats['wifi message tx'] = 'null'
    py_stats['wifi message rx'] = 'null'
    py_stats['v1 open command'] = 'null'
    py_stats['v2 open command'] = 'null'
    py_stats['v3 open command'] = 'null'
    py_stats['v4 open command'] = 'null'
    py_stats['v5 open command'] = 'null'
    py_stats['coil on command'] = 'null'
    py_stats['cal command'] = 'null'
    py_stats['test command'] = 'null'
    py_stats['BM command'] = 'null'

    pi_stats["valve 1 fb"] = 'null'
    pi_stats["valve 2 fb"] = 'null'
    pi_stats["valve 3 fb"] = 'null'
    pi_stats["valve 4 fb"] = 'null'
    pi_stats["valve 5 fb"] = 'null'
    pi_stats["coil fb"] = 'null'
    pi_stats["pt 1 fb"] = 'null'
    pi_stats["pt 2 fb"] = 'null'
    pi_stats["pt 3 fb"] = 'null'
    pi_stats["pt 4 fb"] = 'null'
    pi_stats["pt 5 fb"] = 'null'
    pi_stats["lc fb"] = 'null'
    pi_stats["thermo 1 fb"] = 'null'
    pi_stats["thermo 2 fb"] = 'null'
    pi_stats["abort pt 1 "] = 'null'
    pi_stats["abort pt 2 "] = 'null'
    pi_stats["abort pt 3 "] = 'null'
    pi_stats["abort pt 4 "] = 'null'
    pi_stats["abort pt 5 "] = 'null'
    pi_stats["abort pt 6 "] = 'null'
    py_stats['cal command fb'] = 'null'
    py_stats['test command fb'] = 'null'
    py_stats['BM command fb'] = 'null'
    # still to be updated

    # ToDo Fill in the feedback list

    sys_stats.update(py_stats, **pi_stats)

    def get_pi_status(self):
        return self.pi_stats

    def get_py_status(self):
        return self.py_stats

    @classmethod
    def get_sys_status(self):
        id = 0
        keys = list(self.sys_stats.keys())
        values = list(self.sys_stats.values())

        max_key_length = max(len(key) for key in keys)

        for i in range(len(keys)):
            print(f'{keys[i].ljust(max_key_length)} : {values[i]}')
        return self.sys_stats


class Wifi_Host:
    def __init__(self, port):
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to external IP (Google DNS)
        ip = s.getsockname()[0]
        s.close()
        print(ip)
        self.host = ip
        self.port = port
        self.server_socket = None
        self.connection = None
        self.addy = None
        '''


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


# processes incoming data and forms outgoing data packets
class Telemetry:
    def __init__(self, sys):
        # default
        # 32 bits for 32 commands -> bitwise operations for processing
        self.heartbeat = -49  # checksum for verification
        self.coil_speed = 80  # default coil speed
        self.data = [[0], [0], [0], [0], [0], [0],[0],[0]]
        # self.wifi       = wifi
        self.sys = sys

        # data packet       v1     v2    v3    v4   C     T     CS     A
        #self.data_packet = [0], [0], [0], [0], [0], [0], [0]]
        self.data_packet = [0,0,0,0,0,0,0,0]
        self.rx_data = []
        # connects to ESP32
        #self.sock = BT.connect_to_esp32()
        # all this class does is set and clear bits for the fized data packets coming in and out

        ''' 
        Data out
        byte                         bits
        [heartbeat]||[valve1][valve2][valve3][valve4][coil]|[coil speed]
        '''

    # add heartbeat -> header for data
    def set_coil(self, ms):
        self.coil_speed = ms
        self.data_packet[CS] = [ms]
        return 0

    def send_data(self):
        # self.wifi.send_command(self.send_data_out())
        #BT.send_data(self.sock, self.data_packet)
        print(self.data_packet)
        uart_code1.send_message(self.data_packet)

        return 0
        
    
    # function that starts processing the incoming data
    def get_data(self):
        print('reading')
        msg = uart_code1.receive_response()
        print('recieved')
        print(msg)
        return msg
        '''
        # rx = self.wifi.recieve_data()
        #s#elf.rx_data = BT.receive_data(self.sock)
        self.rx_data = uart_code1.receive_response()
        print(self.rx_data)
        print("hi")
        asr = self.rx_data[1].decode("latin-1")
        
        #print(self.rx_data[1].hex())
        print("bye")
        print(asr)
        
        print("hello")
        asr = b''.join(self.rx_data)
        text = asr.decode('latin-1')
        lines = text.strip().split('\r\n')
        print(lines)
        
        
        # add processing code from byte data to string here
        #data_str = b''.join(self.rx_data).decode('Latin1')
    # Split the string at the CRLF sequences
    
        tokens = data_str.split('\r\n')
        float_list = []
        for token in tokens:
            token = token.strip()# Remove any extraneous whitespace
            # Make sure it's not an empty string
            if token:
                try:
                    value = float(token)
                    if value < 0:
                        value = 123456.5
                    float_list.append(value)
                # Convert the token to a float and add it to the list
                #numbers.append(token)
                #float_list = []
                #for i in numbers[1:]:
                    #new_data = float(i)
                    #float_list.append(i)
                    
                #data = numbers[1:]
                #new_data = float(data)
                except ValueError:
                # If conversion fails, print a warning and skip this token
                    print(f"Warning: Could not convert '{token}' to a float.")
        return float_list
            #return self.rx_data
    '''
        

    # index 0
    def open_valve(self, num):
        # set msb
        # this should be handled at the get data section of the code
        '''
        match num:
            case 1:
                return ser.writelines('v1')
            case 2:
                return ser.writelines('v2')
            case 3:
                return ser.writelines('v3')
            case 4:
                return ser.writelines('v4')
        '''
        if(num == V1):
            self.data_packet[num] = [1]
        if(num == V2):
            self.data_packet[num] = [2]
        if(num == V3):
            self.data_packet[num] = [3]
        if(num == V4):
            self.data_packet[num] = [4]
            
        System_Health.py_stats["v f'{num} open command"] = 'good'
        return 0

    def close_valve(self, num):
        # clear msb
        if(num == V1):
            self.data_packet[num] = ["!"]
        if(num == V2):
            self.data_packet[num] = ["@"]
        if(num == V3):
            self.data_packet[num] = ["#"]
        if(num == V4):
            self.data_packet[num] = ["$"]
        System_Health.py_stats["v{num} open command"] = 'bad'
        return 0

    def spark_coil(self):
        self.data_packet[C] = [9]
         #System_Health.py_stats["v{num} open command"] = 'bad'  # status gets cleared from pi side
        return 0

    def start_test(self):
        #self.data_packet[T] = ['5']
        print("*start test- > needs to be finished")
        return 0

        
    def abort(self):
        #self.data_packet[A] = ['7']
        self.data_packet[V3] = ["#"]
        self.data_packet[V1] = [1]
        self.data_packet[V4] = ["$"]
        time.sleep(0.5)   
        self.data_packet[V2] = ["@"]
        return 0
        print('pycode abort')

        #uart_code1.send_message(self.data_packet)

    def upload_test_sequence(self, file_path):
        # parse excel test sequence
        # print("upload test sequence")
        ts = test_sequence(file_path)
        td = ['TEST']
        td = ts.parse_test()
        BT.send_data(self.sock, td)
        td = ts.parse_abort_limit()
        BT.send_data(self.sock, td)


# collects data and visualizes it for System_Health analysis

# todo finish this class
class Metrics:
    def __init__(self):
        print("metrics")



t = 0
#for i in range(100):
 #uart_code1.send_message(str(t % 4))
 #t +=1

for i in range(2):
    sys = System_Health
    tel = Telemetry(sys)
    #data = tel.get_data()
    #print(data)













            
