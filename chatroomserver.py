import socket
import threading

# Server configuration
server_ip = 'localhost'  # Use your server's IP address here or 'localhost' for local testing
server_port = 5000       # Choose a free port number
max_clients = 10         # Maximum number of players allowed to connect

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(max_clients)

# List to keep track of connected clients
clients = []

def handle_client(client_socket, client_address):
    # Send a welcome message to the client
    client_socket.send(b"Welcome to the chatroom! Type 'exit' to leave.\n")

    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')

            # Broadcast the message to all connected clients
            for client in clients:
                if client != client_socket:
                    client.send(message.encode('utf-8'))
        except:
            # Client disconnected
            print(f"Player {client_address} disconnected.")
            clients.remove(client_socket)
            client_socket.close()
            break

# Main loop to accept incoming client connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Player {client_address} connected.")
    clients.append(client_socket)

    # Start a new thread to handle the client
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
