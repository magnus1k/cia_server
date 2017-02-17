import http.server
import qrcode
import os
import socket
import socketserver
import urllib.parse


class CiaUrl:
    def __init__(self, filename):
        self.file_name = filename
        self.url = "http://{}:{}".format(my_ip, PORT) + urllib.parse.quote("/{}".format(self.file_name).replace("\\", "/"))
        self.qr_file = False

    def make_qrcode(self):
        img = qrcode.make(self.url)
        img.save(self.file_name+".png")
        self.qr_file = True

my_ip = socket.gethostbyname(socket.gethostname())

PORT = 8000
DIR = "C:\\Users\\c14ph\\Documents\\勇气默示录2：终结次元"


def run_server():
    os.chdir(DIR)

    cia_list = dict()

    all_dirs = os.walk(DIR)
    for root, dirs, files in all_dirs:
        for file_name in files:
            name, ext = os.path.splitext(file_name)
            if ext.lower() == ".cia":
                rel_name = os.path.relpath(os.path.join(root, file_name))
                print(rel_name)
                cia_url = CiaUrl(rel_name)
                cia_list[rel_name] = cia_url

    all_dirs = os.walk(DIR)
    for root, _dirs, files in all_dirs:
        for file_name in files:
            name, ext = os.path.splitext(file_name)
            if ext.lower() == ".png":
                rel_name = os.path.relpath(os.path.join(root, name))
                print(rel_name)
                if rel_name in cia_list:
                    cia_list[rel_name].qr_file = True

    for rel_name in cia_list:
        cia_url = cia_list[rel_name]
        print(cia_url.url)
        if not cia_url.qr_file:
            cia_url.make_qrcode()

    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print("{}:{}".format(my_ip, PORT))
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
