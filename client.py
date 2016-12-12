from socket import error as SocketError
import socket
import sys
import client_functions

HOST, PORT = "localhost", 9999
INVALID_INPUT = "{} is not a proper instruction. Please try again\n"
ALREADY_LOGGED_IN = "Already logged in as {}. Please log out if you want to log in again.\n"

previous_ag_sg_response = ''

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    username = None

    while (True):
        # Connect to server and send data
        data = sys.stdin.readline()
        instruction = data.split(' ')[0]
        response = ''
        if instruction == 'login':
            if is_logged_in(username):
                print(ALREADY_LOGGED_IN.format(username))
                continue
            else:
                login(username, data)
                continue
        elif instruction == 'help':
            print(HELP)
            continue
        elif instruction == 'ag':
            if is_logged_in(username):
                internal_ag(sock, username, data, True)
                continue
            else:
                not_logged_in()
                continue
        elif instruction == 'sg':
            if is_logged_in(username):
                internal_ag(sock, username, data, False)
                continue
            else:
                not_logged_in()
                continue
        elif instruction == 'rg':
            if is_logged_in(username):
                internal_rg(sock, username, data)
                continue
            else:
                not_logged_in()
                continue
        elif instruction == 'logout':
            if is_logged_in(username):
                username = None
                continue
            else:
                not_logged_in()
                continue
        else:
            print(INVALID_INPUT.format(data))
            print(HELP)

#parses previous response to extract gid
def gid_from_gname(gname):
    lines = previous_ag_sg_response.split('\n')
    for line in lines:
        if gname in line:
            return int(line[0:1])



def internal_rg(sock, username, data):
    offset = 0
    gname = data.split(' ')[1]
    gid = gid_from_gname(gname)
    response = rg(username, data, gid, offset)
    offset = offset + 1
    respond_to_server(sock, response)
    received = receive_from_server(sock)

    while(True):
        data = sys.stdin.readline()
        instruction = data.split(' ')[0]
        if instruction.isdigit():
            response = rp(gid, data)
        elif instruction == 'r':
            response = r(data, username, gid)
        elif instruction == 'n':
            response = rg(username, data, gid, offset)
        elif instruction == 'p':
            response = p(username, data, gid)
        elif instruction == 'q':
            break
        else:
            print(INVALID_INPUT.format(data))
            print(HELP)
        respond_to_server(sock, response)
        print(receive_from_server(sock))



def internal_ag(sock, username, is_ag):
    n = 0
    if is_ag:
        previous_ag_sg_response = response = ag(username, data, n)
    else:
        previous_ag_sg_response = response = sg(username, data, n)
    n = n + 1
    respond_to_server(sock, response)
    received = receive_from_server(sock)
    print(received)

    while(True):
        data = sys.stdin.readline()
        instruction = data.split(' ')[0]
        if is_ag and instruction == 's':
            s(username, data)
            continue
        elif instruction == 'u':
            u(username, data)
            continue
        elif instruction == 'r':
            r(username, data, gid)
        elif instruction == 'n':
            if is_ag:
                previous_ag_sg_response = response = ag(username, data, n)
            else:
                previous_ag_sg_response = response = sg(username, data, n)
            n = n + 1
        elif instruction == 'q':
            return
        else:
            print(INVALID_INPUT.format(data))
            print(HELP)
        respond_to_server(sock, response)
        print(receive_from_server(sock))


def receive_from_server(sock):
    try:
        received = str(sock.recv(1024), "utf-8")
    except SocketError as e:
        print(e)

    return received


def respond_to_server(sock, response):
    try:
        sock.sendall(bytes(response + "\n", "utf-8"))
    except SocketError as e:
        print(e)
