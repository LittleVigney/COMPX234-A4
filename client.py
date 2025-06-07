class Client:
    def __init__(self, _host, _port, _filelist):
        self.server_host = _host
        self.server_port = _port
        self.filelistname = _filelist
        self.filelist = []

    def start_client():
        pass
    
    def get_filelist(self):
        with open(self.filelistname, 'r') as f:
            for line in f:
                if not line :
                    self.filelist.append(line)
                    