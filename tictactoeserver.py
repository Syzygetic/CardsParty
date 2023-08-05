import socket
import threading
import io
import sys

# Server configuration
server_ip = 'localhost'
server_port = 5000
max_clients = 2  # Two players for Tic-Tac-Toe

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(max_clients)

# List to keep track of connected clients
clients = []
player_symbols = ['X', 'O']

# Initialize the Tic-Tac-Toe board
board = [[' ' for _ in range(3)] for _ in range(3)]

def print_board():
    output = io.StringIO()
    sys.stdout = output

    print("   1   2   3")
    print("1  {} | {} | {}".format(board[0][0], board[0][1], board[0][2]))
    print("  ---+---+---")
    print("2  {} | {} | {}".format(board[1][0], board[1][1], board[1][2]))
    print("  ---+---+---")
    print("3  {} | {} | {}".format(board[2][0], board[2][1], board[2][2]))

    sys.stdout = sys.__stdout__  # Reset the standard output

    return output.getvalue()

def send_to_all(message):
    for client in clients:
        client.send(message.encode('utf-8'))

def handle_client(client_socket, client_address):
    global current_player
    # Assign a player symbol to the client
    player_id = clients.index(client_socket)
    player_symbol = player_symbols[player_id]

    # Send player symbol to the client
    client_socket.send(f"You are Player {player_id + 1} ({player_symbol})".encode('utf-8'))

    # Notify the client about the other player if both players have connected
    if len(clients) == max_clients:
        client_socket.send("\n\nThe other player is making a move. Please wait ...".encode('utf-8'))

    while True:
        try:
            # Wait for the player's turn
            if clients.index(client_socket) == current_player:
                # Send the current board state to the player
                current_board = print_board()
                client_socket.send("\n\nCurrent Board:\n".encode('utf-8'))
                client_socket.send(current_board.encode('utf-8'))

                client_socket.send("\nIt's your turn. Enter a number (1-9) to make a move:".encode('utf-8'))
                move = int(client_socket.recv(1024).decode('utf-8')) - 1

                # Check if the move is valid
                if 0 <= move < 9 and board[move // 3][move % 3] == ' ':
                    board[move // 3][move % 3] = player_symbol

                    # Check if the player wins
                    if check_winner(player_symbol):
                        send_to_all(f"\nPlayer {player_id + 1} ({player_symbol}) wins!")
                        send_to_all("Winning Board:")
                        send_to_all(print_board())
                        send_to_all("Game Over.")
                        break

                    # Check if the game is a tie
                    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
                        send_to_all("It's a tie!")
                        send_to_all("Game Over.")
                        break

                    # Switch to the next player
                    current_player = (current_player + 1) % len(clients)

                    # Notify the other player about the current player's move
                    client_socket.send("\n\nThe other player is making a move. Please wait ...".encode('utf-8'))
                else:
                    client_socket.send("Invalid move. Try again.".encode('utf-8'))
        except:
            # Client disconnected
            print(f"Player {client_address} disconnected.")
            clients.remove(client_socket)
            client_socket.close()
            break

def check_winner(symbol):
    # Check rows, columns, and diagonals for a win
    return any(all(board[i][j] == symbol for i in range(3)) for j in range(3)) or \
           any(all(board[i][j] == symbol for j in range(3)) for i in range(3)) or \
           all(board[i][i] == symbol for i in range(3)) or \
           all(board[i][2 - i] == symbol for i in range(3))

# Main loop to accept incoming client connections
current_player = 0
while len(clients) < max_clients:
    client_socket, client_address = server_socket.accept()
    print(f"Player {client_address} connected.")
    clients.append(client_socket)

    # Start a new thread to handle the client
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
