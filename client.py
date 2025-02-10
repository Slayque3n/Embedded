import socket
import network

# Wi-Fi Configuration
SSID = 'sus'
PASSWORD = 'suspassword'
ip=0
def connectwifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    ip = wlan.ifconfig()[0]
    print(f"Connected to Wi-Fi with IP: {ip}")

while ip == 0:
    connectwifi(SSID, PASSWORD)

# Client Functionality
def start_client(host='0.0.0.0', port=8080):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    try:
        while True:
            message = input("Enter message to send: ")
            if message.lower() == 'exit':
                break
            client.send(message.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()
