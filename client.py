from socket import error as SocketError
import socket
import sys
from client_functions import sg, is_logged_in, login, HELP,not_logged_in

HOST, PORT = "localhost", 9999
INVALID_INPUT = "{} is not a proper instruction. Please try again\n"
ALREADY_LOGGED_IN = "Already logged in as {}. Please log out if you want to log in again.\n"


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    username = None

    while(True):
        # Connect to server and send data
        data = sys.stdin.readline()
        instruction = data.split(' ')[0]
        response=''
        if instruction == 'login':
            if is_logged_in(username):
                print(ALREADY_LOGGED_IN.format(username))
            else:
                login(username, data)
                continue
        elif instruction == 'help':
            print(HELP)
            continue
        elif instruction == 'ag':
            if is_logged_in(username): 
                response=ag(data, username)
            else:
                not_logged_in()
        elif instruction == 'sg':
            if is_logged_in(username):
                response=sg(data, username)
            else:
                not_logged_in()
        elif instruction == 'rg':
            if is_logged_in(username):
                pass
            else:
                not_logged_in()
        elif instruction == 'logout':
            if is_logged_in(username):
                username = None
            else:
                not_logged_in()
        else:
            print(INVALID_INPUT.format(data))

        try:
            sock.sendall(bytes(response + "\n", "utf-8"))
        
            # Receive data from the server
            received = str(sock.recv(1024), "utf-8")
        except SocketError as e:
            print(e)

