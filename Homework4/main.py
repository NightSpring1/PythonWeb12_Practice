import urllib.parse
import mimetypes
import socket
import json
import datetime
from pathlib import Path
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

HTTP_IP = ''
HTTP_PORT = 3000


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('html/index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('html/message.html')
        else:
            if Path(f'.{pr_url.path}').exists():
                self.send_static()
            else:
                self.send_html_file('html/error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(data, (UDP_IP, UDP_PORT))
        self.send_response(302)
        self.send_header('Location', 'html/message.html')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'html')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


class UDPServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()

    def listen_data(self):
        while True:
            data, address = self.sock.recvfrom(4096)
            data_parse = urllib.parse.unquote_plus(data.decode())
            self.write_data(data_parse)

    @staticmethod
    def write_data(data_parse: str):
        input_data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        dict_to_write = {str(datetime.datetime.now()): input_data_dict}

        storage_path = Path('./storage/data.json')
        if not storage_path.exists():
            open(storage_path, 'a').close()

        with open(storage_path, 'r+') as file:
            if storage_path.stat().st_size != 0:
                data_dict = json.load(file)
            else:
                data_dict = {}
            data_dict.update(dict_to_write)
            file.seek(0)
            json.dump(data_dict, file, indent=4)


def run_udp_server(ip, port):
    with UDPServer(ip, port) as server:
        server.listen_data()


def run_http_server(ip, port):
    HTTPServer((ip, port), HttpHandler).serve_forever()


if __name__ == '__main__':
    threads = []

    http_thread = Thread(target=run_http_server, args=(HTTP_IP, HTTP_PORT))
    http_thread.start()
    threads.append(http_thread)

    udp_thread = Thread(target=run_udp_server, args=(UDP_IP, UDP_PORT))
    udp_thread.start()
    threads.append(udp_thread)

    [el.join() for el in threads]
