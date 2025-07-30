import logging
import asyncio
import json

from kademlia.network import Server

# Set up logging
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

# Initialize bootstrap addresses list
bootstrap_addresses = []

# Read bootstrap nodes from configuration file
try:
    with open('config/bootstrap_nodes.json', 'r') as f:
        bootstrap_nodes = json.load(f)
        bootstrap_addresses = [(node['address'].split(':')[0], int(node['address'].split(':')[1])) for node in bootstrap_nodes]
except FileNotFoundError:
    bootstrap_nodes = []
except json.decoder.JSONDecodeError:
    bootstrap_nodes = []

server = Server()

loop = asyncio.get_event_loop()
loop.set_debug(True)

if bootstrap_nodes:
    async def main():
        await server.listen(8468)  # Your node's port
        if bootstrap_addresses:
            await server.bootstrap(bootstrap_addresses)
else:
    loop.run_until_complete(server.listen(8468))


try:
    if bootstrap_nodes:
        loop.run_until_complete(main())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.stop()
    loop.close()
