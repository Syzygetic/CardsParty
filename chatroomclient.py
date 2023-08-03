import socket
import threading

# Client configuration
server_ip = 'localhost'  # Use your server's IP address here or the server's IP if it's running on a different machine
server_port = 5000       # Use the same port number as the server

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Function to receive and display messages from the server
def receive_messages():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

# Start a separate thread to receive messages
threading.Thread(target=receive_messages).start()

# Main loop to read user input and send messages to the server
while True:
    message = input()
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode('utf-8'))

# Close the client socket when done
client_socket.close()
