import serial
import time

# Set the correct serial port (e.g., '/dev/ttyACM0')
arduino_port = '/dev/ttyACM0'  
baud_rate = 9600  # Match the baud rate to the Arduino

# Open the serial connection to the Arduino
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on port {arduino_port}")
except serial.SerialException as e:
    print(f"Error connecting to the Arduino: {e}")
    exit()

time.sleep(2)  # Wait for the connection to establish

def send_message(message):
    """
    Send a message one character at a time to the Arduino
    with delimiters as per the request (e.g., "[" "H" "," "e" ",").
    """
    ser.reset_output_buffer()
    for char in message:
        # Send '['
        ser.write('['.encode())  
        print(f"Sent: [")
        time.sleep(0.05)
        
        # Send the character
        print(type(char))
        print(char)
        ser.write(str(char).encode())
        print(f"Sent: {char}")
        time.sleep(0.05)
        
        # Send ','
        ser.write(','.encode())  
        print(f"Sent: ,")
        time.sleep(0.05)

def receive_response():
    """
    Receive data from the Arduino.
    This function reads the response one character at a time.
    """
    print('Recieving Response')
    rx_data = []
    ser.reset_input_buffer()
    ser.write(b'5')
    opd01_response = ser.readline().decode('Latin1').strip()
    '''
    print(type(opd01_response))
    
    These valuescomefromthe arduino as strings so they need to
    be converted.
    '''
    opd01_response = float(opd01_response)
    rx_data.append(opd01_response)
    ser.write(b'6')
    time.sleep(0.0001)
    opd02_response = ser.readline().decode('Latin1').strip()
    opd02_response = float(opd02_response)
    rx_data.append(opd02_response)
    ser.write(b'7')
    time.sleep(0.0001)
    epd01_response = ser.readline().decode('Latin1').strip()
    epd01_response = float(epd01_response)
    rx_data.append(epd01_response)
    ser.write(b'8')
    time.sleep(0.0001)
    fpd01_response = ser.readline().decode('Latin1').strip()
    fpd01_response = float(fpd01_response)
    rx_data.append(fpd01_response)
    return rx_data
    '''
    for i in range(30):  # Check if data is available
        #received_char = ser.read().decode('Latin1')  # Read one byte
        received_char = ser.read()  # Read one byte
        print('HERE')
        rx_data.append(received_char)
    return rx_data
    '''
'''
def main():
    try:
        while True:
            message = "[1,2,3,4,!,@,#,$]"  # Example message to send
            send_message(message)  # Send the message to Arduino

            # Receive the response from Arduino
            time.sleep(1)  # Wait for Arduino to echo back all characters

    except KeyboardInterrupt:
        print("Communication terminated by user.")
    finally:
        if ser.is_open:
            ser.close()  # Close the serial port when done
            print("Serial port closed.")

if __name__ == "
'''

