import logging
import asyncio
import sys

from kademlia.network import Server



handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

async def run():
    server = Server()
    await server.listen(8440)
    bootstrap_node = ("10.151.0.1", 8474)
    await server.bootstrap([bootstrap_node])

    result = await server.get("chat2")
    print("Get result:", result)
    server.stop()

asyncio.run(run())
