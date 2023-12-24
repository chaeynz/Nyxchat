from modules.connection_handler import ConnectionHandler
import modules.dht

from modules.message import Message

# pylint: disable=all

class NetworkEngine:
    """
    Central abstracted engine class for interacting with the peer-to-peer network
    """
    _self = None


    def __init__(self):
        self.connection_handler = ConnectionHandler()


    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self


    def send_message(self, message:Message):
        self.connection_handler.send(data=str(message), address=self.dht[message.recipient_id])


    def syn_send_message(self, message:Message):
        self.connection_handler.syn_send(data=message.content, address=dht.find_ip_of_user(message.recipient_id))
