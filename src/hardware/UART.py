'''
Creators: Izuka 
'''

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
    for char in message:
        # Send '['
        ser.write('['.encode())
        print(f"Sent: [")
        time.sleep(0.1)

        # Send the character
        ser.write(char.encode())
        print(f"Sent: {char}")
        time.sleep(0.1)

        # Send ','
        ser.write(','.encode())
        print(f"Sent: ,")
        time.sleep(0.1)


def receive_response():
    """
    Receive data from the Arduino.
    This function reads the response one character at a time.
    """
    if ser.in_waiting > 0:  # Check if data is available
        received_char = ser.read().decode('utf-8')  # Read one byte
        print(f"Received: {received_char}")
        return received_char
    return None  # No data received


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


if __name__ == "__main__":
    main()
