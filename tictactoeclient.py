import socket

# Client configuration
server_ip = 'localhost'
server_port = 5000

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Function to receive and display messages from the server
def receive_messages():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

# Start a separate thread to receive messages
import threading
threading.Thread(target=receive_messages).start()

# Main loop to read user input and send messages to the server
while True:
    message = input()
    client_socket.send(message.encode('utf-8'))

# Close the client socket when done
client_socket.close()
