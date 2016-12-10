import socket
import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        welcome_message = "Welcome to hlp forum!"
        self.request.sendall(welcome_message)

        while(True):
            #TODO: Add functions for server operations.
            data = str(self.request.recv(1024), 'ascii')


            # data = str(self.request.recv(1024), 'ascii')
            # cur_thread = threading.current_thread()
            # response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
            # self.request.sendall(response)

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