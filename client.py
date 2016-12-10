from socket import error as SocketError
import socket
import sys

HOST, PORT = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while(True):
        # Connect to server and send data
        data = sys.stdin.readline()
        instruction = data.split(' ')[0]
        if instruction == 'login':
            pass
        elif instruction == 'help':
            pass
        elif instruction == 'ag':
            pass
        elif instruction == 'sg':
            pass
        elif instruction == 'rg':
            pass
        elif instruction == 'logout':
            pass
        
        try:
            sock.sendall(bytes(data + "\n", "utf-8"))
        
            # Receive data from the server
            received = str(sock.recv(1024), "utf-8")
        except SocketError as e:
            print(e)


        print("Sent:     {}".format(data))
        print("Received: {}".format(received))