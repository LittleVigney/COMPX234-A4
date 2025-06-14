import socket
import threading
import os
import random
import base64

class Server:
    def __init__(self, _port):
        self.port = _port
        self.files = "server_file/"

    def start_server(self):
        print("Server running...")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind(("localhost", self.port))

            # wait for request
            while True:
                rq, client_addr = server_socket.recvfrom(1024)
                rq = rq.decode().strip()
                rq = rq.split()

                # if client want to download, create thread and handle the client
                if rq[0] == "DOWNLOAD":
                    if len(rq) == 2:
                        filename = rq[1]
                        threading.Thread(target=self.handle_client, args=(filename, client_addr)).start()

    def handle_client(self, filename, client_addr):
        file_path = os.path.join(self.files, filename)

        # if the file client want to download is not existed
        if not os.path.exists(file_path):
            # send error to client
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as error_socket:
                error_message = f"ERR {filename} NOT_FOUND"
                error_socket.sendto(error_message.encode(), client_addr)
                return

        # if file exists
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_port = random.randint(50000, 51000)
            file_size = os.path.getsize(file_path)

            # send ok message to client
            client_socket.bind(("localhost", client_port))
            res_message = f"OK {filename} SIZE {file_size} PORT {client_port}"

            self.send_res(client_socket, res_message, client_addr)

            # send block data to client
            with open(file_path, 'rb') as f:
                while True:
                    rq, addr = client_socket.recvfrom(1024)
                    rq = rq.decode().strip()

                    rq_lst = rq.split()
                    
                    # if client want to close
                    if rq_lst[2] == "CLOSE":
                        close_message = f"FILE {filename} CLOSE_OK"

                        self.send_res(client_socket, close_message, addr)
                    # if client want to download data block
                    elif rq_lst[2] == "GET":
                        start_num = int(rq_lst[rq_lst.index("START") + 1])
                        end_num = int(rq_lst[rq_lst.index("END") + 1])

                        # check whether the range of request is legal
                        if start_num <= file_size - 1 and end_num <= file_size - 1:
                            f.seek(start_num)
                            res_packet = f.read(end_num - start_num + 1)

                            # encode data and send it to client
                            packet_data = base64.b64encode(res_packet).decode()
                            packet_message = f"FILE {filename} OK START {start_num} END {end_num} DATA {packet_data}"
                            self.send_res(client_socket, packet_message, addr)

    def send_res(self, socket, message, addr):
        socket.sendto(message.encode(), addr)


if __name__ == "__main__":
    server = Server(51234)
    server.start_server()
