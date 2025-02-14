import socket
import threading
from databse import initialize_database
from databse import print_database 
import sqlite3
import time

# Server Functionality
def handle_client(client_socket, address):
    print(f"Connection established with {address}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {address}: {message}")
            client_socket.send("Message received".encode('utf-8'))
            id,data=message.split(":")
            type,value=data.split(",")
            conn = sqlite3.connect("plant_management.db")
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO Changes (plant_id, change_description, value) VALUES (?, ?, ?)""", (id, type, value))
            conn.commit()
            conn.close()


        except:
            print(f"Connection closed with {address}")
            break
    client_socket.close()

def start_server(host="192.168.236.160", port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    print(socket.gethostbyname(socket.gethostname()))
    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()
        time.sleep(0.01)

if __name__ == "__main__":
    
    initialize_database()
    start_server()
 
