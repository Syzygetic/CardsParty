import socket

server_ip = 'localhost'  # Use your server's IP address here or the server's IP if it's running on a different machine
server_port = 5000       # Use the same port number as the server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
