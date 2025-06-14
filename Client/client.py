import socket
import time
import os

class Client:
    def __init__(self, _port, _filelist):
        self.server_host = "localhost"
        self.server_port = _port
        self.filelistname = _filelist
        self.filelist = []
        self.timeout = 1
        self.retransmit_time = 5

    def start_client(self):
        # get names of files from txt file
        self.get_filelist()

        # download every file
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            # send request for every file name
            for every_file in self.filelist:
                print(every_file)
                self.download_file(every_file, client_socket, (self.server_host, self.server_port))
    
    def get_filelist(self):
        with open(self.filelistname, 'r') as f:
            for line in f:
                if line :
                    self.filelist.append(line)

    def download_file(self, filename, client_socket, server_addr):
        dl_message = f"DOWNLOAD {filename}"

        # get reponse from server
        res = self.send_rq(dl_message, client_socket, server_addr)

        print(res) 

        # if not found
        if res[0 : 4] == "ERR":
            print("File downloading failed.")
            return

        # if file found
        res_part = res.split()
        file_size = res_part[res_part.index("SIZE") + 1]
        port = res_part[res_part("PORT") + 1]

        downloaded_file = os.path.join(filename)
        with open(downloaded_file, 'w') as f:
            file_ct = 0

            while file_ct <= file_size:
                start_num = file_ct
                end_num = start_num + 999

                packet_message = f"FILE {filename} GET START {start_num} END {end_num}"
                res_packet = self.send_rq(packet_message, client_socket, (self.server_host, port))

                if "OK START" in res_packet:
                    packet_data = res_packet[res_packet.find("DATA")] + 5

                    f.write(packet_data)

                    file_ct += len(packet_data)
                else:
                    pass

            close_message = f"FILE {filename} CLOSE"
            res_close = self.send_rq(client_socket, client_socket, (self.server_host, port))

            if "CLOSE_OK" in res_close:
                print("File downloading finished.")
            else:
                print("File downloading failed.")


    def send_rq(self, message, client_socket, server_addr):
        for retrans in range(self.retransmit_time):
            try:
                client_socket.settimeout(self.timeout / 1000)

                client_socket.sendto(message.encode('utf-8'), server_addr)
                res = client_socket.recvfrom(1024)

                return res.decode('utf-8')
            except socket.timeout:
                continue

if __name__ == "__main__":
    port = int(input("Input port for client: "))
    file_list = input("Input the name of file list: ")

    client = Client(port, file_list)
    client.start_client()
    