import socket
import threading

class Server:
    def __init__(self, _port):
        self.port = _port

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind(("localhost", self.port))

            while True:
                rq, client_addr = server_socket.recvfrom(1024)
                rq = rq.decode().strip()

                if rq[ : 8] == "DOWNLOAD":
                    filename = rq[8 : ]

                    if filename is not None:
                        threading.Thread(target=self.handle_client, args=(filename, client_addr)).start()

    def handle_client(self, filename, client_addr):
        