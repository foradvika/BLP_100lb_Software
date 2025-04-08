#Creator: Izuka
import socket

ESP32_MAC = "40:91:51:2C:FE:FE"  # Replace with actual ESP32 MAC
RFCOMM_PORT = 1


class BT:

    def connect_to_esp32():
        print(f"🔗 Connecting to ESP32 at {ESP32_MAC}...")

        try:
            sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            sock.connect((ESP32_MAC, RFCOMM_PORT))
            print("✅ Connected successfully!")

            return sock
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return None

    def send_data(sock, data_packet):
        indx = 0
        for i in data_packet:
            """Send an integer array formatted as a packet, ignoring NoneType values."""
            print(data_packet[indx])
            packet_str = ",".join(map(str, data_packet)) + "\n"  # Convert to comma-separated string\
            indx += 1
        print("SIZE = " + str(len(packet_str.encode())))
        sock.sendall(packet_str.encode())  # Send the encoded packet
        print("📤 Sent Data Packet:", packet_str)

    def receive_data(sock):
        """Receive full message from ESP32."""
        try:
            data = sock.recv(1024).decode().strip()  # Read incoming data
            if data:
                print("📩 Received from ESP32:", data)
                parsed_values = list(map(int, data.split(",")))  # Convert received data to integers
                print("✅ Parsed Values:", parsed_values)
        except Exception as e:
            print(f"⚠️ Error receiving data: {e}")

        return data


'''
if __name__ == "__main__":
    sock = connect_to_esp32() # wifi module init
    data_packet = [1,2,3,4,5,6,7,8,9,10] # telem packet
    print(data_packet[2])
    if sock:
        try:
            send_data(sock, data_packet)
            while True:
                data = receive_data(sock)
        except KeyboardInterrupt:
            print("\n🔌 Closing connection...")
        finally:
            sock.close()
'''
