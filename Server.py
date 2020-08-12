import socket
import threading

from http.server import HTTPServer

from RequestHandler import RequestHandler

HOST = ''
PORT = 8001

class Server:
    def __init__(self):

        def create_handler(*args):
            RequestHandler(*args)

        server = HTTPServer((HOST, PORT), create_handler)
        print(f'Server up at {HOST}:{PORT}')

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

        print('Closing server...')
        server.server_close()