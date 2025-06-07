import socket
import time

class Client:
    def __init__(self, _host, _port, _filelist):
        self.server_host = _host
        self.server_port = _port
        self.filelistname = _filelist
        self.filelist = []
        self.timeout = 1

    def start_client(self):
        # get names of files from txt file
        self.get_filelist(self)

        # download every file
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            # send request for every file name
            pass
    
    def get_filelist(self):
        with open(self.filelistname, 'r') as f:
            for line in f:
                if not line :
                    self.filelist.append(line)

    def download_file(self, filename, client_socket, server_addr):
        dl_message = f"DOWNLOAD f{filename}"

        # get reponse from server
        

    def send_rq(self, dl_message, client_socket, server_addr):
        while True:
            try:
                client_socket.settimeout(self.timeout / 1000)

                client_socket.sendto(dl_message.encode('utf-8'), server_addr)
                res = client_socket.recvfrom(1024)

                return res.decode('utf-8')
            except socket.timeout:
                