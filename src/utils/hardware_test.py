import serial
import time
from serial_pc import BT

def test_hardware_connection():
    print("Testing hardware connection...")
    
    # Try to connect to ESP32
    try:
        sock = BT.connect_to_esp32()
        if sock:
            print("✅ Successfully connected to ESP32")
        else:
            print("❌ Failed to connect to ESP32")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

    # Test basic valve commands
    test_commands = [
        [1, 0, 0, 0, 0, 0, 0, 0],  # Open valve 1
        [0, 1, 0, 0, 0, 0, 0, 0],  # Open valve 2
        [0, 0, 1, 0, 0, 0, 0, 0],  # Open valve 3
        [0, 0, 0, 1, 0, 0, 0, 0],  # Open valve 4
        [0, 0, 0, 0, 0, 0, 0, 0],  # Close all valves
    ]

    print("\nTesting valve commands...")
    for i, cmd in enumerate(test_commands):
        try:
            print(f"Sending command {i+1}: {cmd}")
            BT.send_data(sock, cmd)
            time.sleep(1)  # Wait for response
            response = BT.receive_data(sock)
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error sending command {i+1}: {e}")
            return False

    print("\n✅ Basic hardware test completed successfully")
    return True

if __name__ == "__main__":
    test_hardware_connection() 