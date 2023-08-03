import socket
import threading

server_ip = 'localhost'  # Use your server's IP address here or 'localhost' for local testing
server_port = 5000       # Choose a free port number

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(4)  # Allow up to 2 players to connect
print("Server is ready to accept connections.")

def handle_client(client_socket, player_id):
    # Implement game logic and communication with the player here
    pass

player_id = 1
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Player {player_id} connected from {client_address}")
    # Start a new thread to handle the client
    threading.Thread(target=handle_client, args=(client_socket, player_id)).start()
    player_id += 1

