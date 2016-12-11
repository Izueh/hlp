import socket
import threading
import socketserver

INVALID_INPUT = "{} is not a proper instruction. Please try again\n"

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        welcome_message = "Welcome to hlp forum!"
        self.request.sendall(welcome_message)
        response = ''

        while(True):
            
            data = str(self.request.recv(1024), 'ascii')
            instruction = data.split(' ')[0]
            if instruction == 'sg':
                response = sg(data)
            elif instruction == 'ag':
                response = ag(data)
            else:
                self.request.sendall(bytes(INVALID_INPUT.format(data)))
                continue

            self.request.sendall(bytes(response))
            

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

    while(True):
        #TODO: add parse for closing server on main thread
        pass 

    server.shutdown()
    server.server_close()