# pylint: disable=all

from kademlia.network import Server

def find_ip_of_user(user_id:str):
    return '127.0.0.1'

class DHT:
    def __init__(self, port,):
        self.port = port
        self.node = Server()
        

    async def bootstrap(self, user_id:str):
        await self.node.bootstrap([('127.0.0.1', self.port)])
        await self.node.set(user_id, )

    async def start_listen(self):
        await self.node.listen(self.port)