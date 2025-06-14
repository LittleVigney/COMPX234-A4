import socket
import threading
import os
import random

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
        file_path = os.path.join(filename)

        if not file_path:
            # send error
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as error_socket:
                error_message = f"ERR {filename} NOT_FOUND"
                error_socket.sendto(error_message.encode(), client_addr)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_port = random.randint(50000, 51000)
            file_size = os.path.getsize(file_path)

            client_socket.bind(("localhost", client_port))
            res_message = f"OK {filename} SIZE {file_size} PORT {client_port}"

            self.send_res(client_socket, res_message, client_addr)

            with open(file_path, 'r') as f:
                while True:
                    rq = client_socket.recv(1024)
                    rq = rq.decode().strip()

                    rq_lst = rq.split()

                    if rq_lst[2] == "CLOSE":
                        close_message = f"FILE {filename} CLOSE_OK"

                        self.send_res(client_socket, close_message, client_addr)

                    elif rq_lst[2] == "GET" and rq_lst[3] == "START":
                        start_num = int(rq_lst[rq_lst.index("START") + 1])
                        end_num = int(rq_lst[rq_lst.index("END") + 1])

                        if start_num <= file_size - 1 and end_num <= file_size - 1:
                            f.seek(start_num)
                            res_packet = f.read(end_num - start_num)

                            packet_message = f"FILE {filename} OK START {start_num} END {end_num} DATA {res_packet}"
                            self.send_res(client_socket, packet_message, client_addr)


    def send_res(self, socket, message, addr):
        socket.sendto(message.encode(), addr)