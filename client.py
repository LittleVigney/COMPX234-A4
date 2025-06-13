import socket
import time

class Client:
    def __init__(self, _host, _port, _filelist):
        self.server_host = _host
        self.server_port = _port
        self.filelistname = _filelist
        self.filelist = []
        self.timeout = 1
        self.retransmit_time = 5

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
        dl_message = f"DOWNLOAD {filename}"

        # get reponse from server
        res = self.send_rq(dl_message, client_socket, server_addr)

        # if not found
        if res[0 : 4] == "ERR":
            pass

        # if file found
        res_part = res.split()
        file_size = res_part[res_part.index("SIZE") + 1]
        port = res_part[res_part("PORT") + 1]

        downloaded_file = ""
        with open(downloaded_file, 'w') as f:
            file_ct = 0

            while file_ct <= file_size:
                start_num = file_ct
                end_num = start_num + 999

                packet_message = f"FILE {filename} GET START {start_num} END {end_num}"
                res_packet = self.send_rq(packet_message, client_socket, (self.server_host, port))

                



    def send_rq(self, dl_message, client_socket, server_addr):
        for retrans in range(self.retransmit_time):
            try:
                client_socket.settimeout(self.timeout / 1000)

                client_socket.sendto(dl_message.encode('utf-8'), server_addr)
                res = client_socket.recvfrom(1024)

                return res.decode('utf-8')
            except socket.timeout:
                continue

        