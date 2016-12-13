from socket import error as SocketError
import socket
import sys
from client_functions import is_logged_in, not_logged_in, HELP, login, ag, sg, u, r, p, s, rp, rg

HOST, PORT = "localhost", 9999
INVALID_INPUT = "{} is not a proper instruction. Please try again\n"
ALREADY_LOGGED_IN = "Already logged in as {}. Please log out if you want to log in again.\n"

previous_ag_sg_response = ''


#parses output previously given to user
# @param gname name of group of group to find ID of
# return group_id of provided groupname
def gid_from_gname(gname):
    global previous_ag_sg_response
    lines = previous_ag_sg_response.split('\n')
    for line in lines:
        if gname in line:
            return int(line[0:1])


# loop to consume input for subcommands of rg function
# @param sock socket variable to communicate to server
# @param username username of current user
# @param data raw input given by user
def internal_rg(sock, username, data):
    intial_data = data #to be used in 'n'
    offset = 0
    gname = data.split(' ')[1]
    gid = gid_from_gname(gname)
    response = rg(username, data, gid, offset)
    offset = offset + 1
    respond_to_server(sock, response)
    received = receive_from_server(sock)

    while (True):
        data = sys.stdin.readline()
        instruction = data.split(' ')[0]
        if instruction.isdigit():
            response = rp(gid, data)
        elif instruction == 'r':
            response = r(data, username, gid)
        elif instruction == 'n':
            response = rg(username, intial_data, gid, offset)
        elif instruction == 'p':
            response = p(username, data, gid)
        elif instruction == 'q':
            break
        else:
            print(INVALID_INPUT.format(data))
            print(HELP)
            continue
        respond_to_server(sock, response)
        print(receive_from_server(sock))


# loop to consume input for subcommands of ag and sg functions
# @param sock socket variable to communicate to server
# @param username username of current user
# @param data raw input given by user
# @param is_ag boolean to tell us whether the loop is handling subcommands for
# ag or sg
def internal_ag(sock, username, data, is_ag):
    intial_data = data #to be used in 'n'
    n = 0
    global previous_ag_sg_response
    if is_ag:
        response = ag(username, data, n)
    else:
        response = sg(username, data, n)
    n = n + 1 #DEBUG: n= size+1 should fix this
    respond_to_server(sock, response)
    previous_ag_sg_response = received = receive_from_server(sock)
    print(received)

    while (True):
        data = sys.stdin.readline().rstrip()
        instruction = data.split(' ')[0]
        if is_ag and instruction == 's':
            s(username, data)
            continue
        elif instruction == 'u':
            u(username, data)
            continue
        elif instruction == 'n':
            if is_ag:
                response = ag(username, intial_data, n)
            else:
                response = sg(username, intial_data, n)
            n += 1
            respond_to_server(sock, response)
            previous_ag_sg_response = received = receive_from_server(sock)
            print(received)
        elif instruction == 'q':
            return
        else:
            print(INVALID_INPUT.format(data))
            print(HELP)

# obtain input from server
# @param sock socket variable to communicate with server
def receive_from_server(sock):
    try:
        received = str(sock.recv(1024), "utf-8")
        return received
    except SocketError as e:
        print(e)

# send response to server
# @param sock socket variable to communicate with server
# @param response string to send to server
def respond_to_server(sock, response):
    try:
        sock.sendall(bytes(response, "utf-8"))
    except SocketError as e:
        print(e)


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    #used to keep track of current user
    username = None
    print(receive_from_server(sock))
    while (True):
        # user input
        data = sys.stdin.readline().rstrip()
        instruction = data.split(' ')[0]
        response = ''
        #if/else chain to route for proper usage
        if instruction == 'login':
            if is_logged_in(username):
                print(ALREADY_LOGGED_IN.format(username))
                continue
            else:
                username = login(username, data)
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
