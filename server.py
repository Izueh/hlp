import socket
import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):

        while(True):
            pass
            #TODO: Add functions for client operations.

            # data = str(self.request.recv(1024), 'ascii')
            # cur_thread = threading.current_thread()
            # response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
            # self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
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
        pass #TODO: add parse for closing server

    server.shutdown()
    server.server_close()