import sys
import socket
import asyncio
import selectors
import types

from modules.event_handler import EventHandler

# pylint: disable=missing-docstring

class ConnectionHandler:
    _self = None

    def __init__(self):
        self.chat_port = 1337

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def send(self, data:str, address):
        reader, writer = await asyncio.open_connection(address, self.chat_port)

        writer.write

    async def listen(self):
        # listen forever
        # each full message call back EventHandler.notify("message_received")
        pass

    def syn_send(self, data, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, self.chat_port))

        try:
            data = data.encode()
            sock.sendall(data)
        finally:
            sock.close()

    def syn_listen(self, event_handler:EventHandler, address='0.0.0.0'):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((address, self.chat_port))
            server_socket.listen(1)

            while True:
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    print(f"Connected by {client_address}")

                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break

                        data = data.decode().strip()
                        event_handler.notify('message_received', data)
