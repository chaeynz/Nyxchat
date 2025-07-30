# pylint: disable=missing-docstring, line-too-long
import logging
import asyncio
import random
import json
import re
import threading
import os

from kademlia.network import Server
from modules.user import User
from modules.event_handler import EventHandler

RED = '\033[91m'
RESET = '\033[0m'

LOG_PATH = 'log/'
KADEMLIA_LOG_PATH = f'{LOG_PATH}kademlia.log'
POLLER_LOG_PATH = f'{LOG_PATH}poller.log'
NETENGINE_LOG_PATH = f'{LOG_PATH}netengine.log'

os.makedirs(LOG_PATH, exist_ok=True)



handler = logging.FileHandler(KADEMLIA_LOG_PATH)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
kademlia_log = logging.getLogger('kademlia')
kademlia_log.addHandler(handler)
kademlia_log.setLevel(logging.DEBUG)

handler = logging.FileHandler(POLLER_LOG_PATH)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
poller_log = logging.getLogger('poller')
poller_log.addHandler(handler)
poller_log.setLevel(logging.DEBUG)


handler = logging.FileHandler(NETENGINE_LOG_PATH)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
netengine_log = logging.getLogger('netengine')
netengine_log.addHandler(handler)
netengine_log.setLevel(logging.DEBUG)


def split_ip_port(address):
    # Define the regex pattern to match IP address and port
    pattern = r'^(?P<ip>\d{1,3}(?:\.\d{1,3}){3}):(?P<port>\d+)$'
    match = re.match(pattern, address)
    if match:
        return match.group('ip'), match.group('port')
    else:
        raise ValueError("Invalid address format")


class NetworkEngine:
    _self = None

    def __init__(self):
        self.server = Server()
        self.is_poller_participants_running = False

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def bootstrap(self, bootstrap_node: list[tuple]):
        port = random.randint(8470,8480)
        is_success = False
        while not is_success:
            try:
                await self.server.listen(port)
                is_success = True
            except OSError:
                port = random.randint(8470,8480)

        await self.server.bootstrap(bootstrap_node)


    async def update_location(self, user, endpoint_address, endpoint_port):
        value = {
            'endpoint': f'{endpoint_address}:{endpoint_port}',
            'name': user.name
        }
        netengine_log.info("Setting location of %s to %s", user.id, value)
        await self.server.set(user.id, json.dumps(value))


    async def get_location(self, user: User) -> dict:
        """
        Returns a dict
        'endpoint': endpoint,
        'name': username
        """
        response = await self.server.get(user.id)
        netengine_log.info("DHT response for location of %s is: %s", user.id, response)
        try:
            location = json.loads(response)
        except TypeError:
            location = []

        return location


    async def kill_location(self, user: User) -> dict:
        """
        Returns a dict
        'endpoint': endpoint,
        'name': username
        """
        await self.server.set(user.id, "__DEAD__")
        netengine_log.info("Killed %s on net", user.id)


    async def get_chatroom_participants(self, chatroom_id) -> list:
        participants = await self.server.get(chatroom_id)
        return json.loads(participants) if participants else []


    async def get_chatroom_uparticipants(self, chatroom_id):
        participants = await self.get_chatroom_participants(chatroom_id)

        async def process_participant(user_id):
            participant = User(id=user_id)
            location = await self.get_location(participant)
            if 'endpoint' in location:
                ip, port = split_ip_port(location['endpoint'])
                participant.endpoint_address = ip
                participant.endpoint_port = port
                participant.name = location.get('name')
            return participant

        participants = [await process_participant(user_id) for user_id in participants]
        return participants


    async def get_chatrooms(self) -> list:
        try:
            chatrooms = json.loads(await self.server.get('chatrooms'))
        except TypeError:
            chatrooms = []
        return chatrooms


    async def register_chatroom(self, chatroom_id):
        chatrooms = await self.get_chatrooms()
        if chatroom_id not in chatrooms:
            chatrooms.append(chatroom_id)
            await self.server.set('chatrooms', json.dumps(chatrooms))


    async def join_chatroom(self, user:User, chatroom_id):
        await self.register_chatroom(chatroom_id)

        participants:dict = await self.get_chatroom_participants(chatroom_id)

        if user.id not in participants:
            participants.append(user.id)
        await self.server.set(chatroom_id, json.dumps(participants))
        print(f"Joined chatroom {chatroom_id}")


    async def leave_chatroom(self, user:User, chatroom_id):
        netengine_log.info("Participant %s is trying to leave %s", user.name, chatroom_id)
        participants:dict = await self.get_chatroom_participants(chatroom_id)

        participants = [p for p in participants if p != user.id]


        await self.server.set(chatroom_id, json.dumps(participants))
        print(f"Left chatroom {chatroom_id}")


    async def _loop_poll_participants(self, chatroom_id):
        event_handler = EventHandler()

        while self.is_poller_participants_running:
            polled_participants = await self.get_chatroom_uparticipants(chatroom_id)
            poller_log.debug("Heartbeat: [\"%s\"]", '", "'.join([participant.id for participant in polled_participants]))

            event_handler.notify('PPOLLER_HEARTBEAT', polled_participants)
            await asyncio.sleep(5)


    async def start_polling_participants(self, chatroom_id):
        """Polls chat participants in a separate thread."""
        self.is_poller_participants_running = True

        def run_loop():
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
            loop.run_until_complete(self._loop_poll_participants(chatroom_id))

        listener_thread = threading.Thread(target=run_loop)
        listener_thread.daemon = True  # Ensures thread will close when main program exits
        listener_thread.start()


    def stop_polling_participants(self):
        self.is_poller_participants_running = False


    def terminate(self):
        self.server.stop()
