import sys
import socket
import asyncio
import selectors
import types

# pylint: disable=missing-docstring

class ConnectionHandler:
    _self = None

    def __init__(self):
        self.chat_port = 1337

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def send(self, message:str, host):
        reader, writer = await asyncio.open_connection(host, self.chat_port)

        writer.write

    async def listen(self):
        # listen forever
        # each full message call back EventHandler.notify("message_received")
        pass

    def syn_send(self, data, ip_address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        address = (ip_address, self.chat_port)
        sock.connect(address)

        try:
            data = data.encode()
            sock.sendall(data)
        finally:
            sock.close()