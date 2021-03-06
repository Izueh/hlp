import socket
import threading
import socketserver
import sys
from server_functions import sg,ag ,p ,rp,rg
INVALID_INPUT = "{} is not a proper instruction. Please try again\n"

#class ran by server during serve_forever thread.
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        welcome_message = "Welcome to hlp forum!"
        self.request.sendall(bytes(welcome_message, 'utf-8'))
        response = ''

        while(True):
            
            data = str(self.request.recv(1024), 'utf-8')
            instruction = data.split(' ')[0]
            if instruction == 'sg':
                response = sg(data)
            elif instruction == 'ag':
                response = ag(data)
            elif instruction == 'rg':
                response = rg(data)
            elif instruction == 'p':
                response = p(data)
            elif instruction == 'rp':
                response = rp(data)
            else:
                self.request.sendall(bytes(INVALID_INPUT.format(data), 'utf-8'))
                continue

            self.request.sendall(bytes(response,'utf-8'))
            
# ThreadedTCPServer class. Allows for us to override default parameters.
# Currently using defaults
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":

    HOST, PORT = "localhost", 9999
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    #server-side user input
    while(True):
        data = sys.stdin.readline().rstrip()
        if len(data) > 0:
            instruction = data[0]
            if instruction == 'q':
                break

    server.shutdown()
    server.server_close()