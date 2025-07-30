# pylint: disable=missing-docstring
import logging
import os
from modules.user import User
from modules.network_engine import NetworkEngine
from modules.connection_handler import send_message
from modules.event_handler import EventHandler

LOG_PATH = 'log/'
CHATENGINE_LOG_PATH = f'{LOG_PATH}chatengine.log'

os.makedirs(LOG_PATH, exist_ok=True)

handler = logging.FileHandler(CHATENGINE_LOG_PATH)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
chatengine_log = logging.getLogger('chatengine')
chatengine_log.addHandler(handler)
chatengine_log.setLevel(logging.DEBUG)


class ChatEngine:
    _self = None
    _init = False

    def __init__(self):
        if not ChatEngine._init:
            self.net:NetworkEngine = NetworkEngine._self
            self._user = None
            self._chatroom = None
            self._participants: list[User] = []
            self.event_handler = EventHandler()
            self.event_handler.subscribe("PPOLLER_HEARTBEAT", self.handle_poller_heartbeat)
            ChatEngine._init = True


    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self


    def handle_poller_heartbeat(self, participants: list[User]):
        chatengine_log.debug("handle_poller_heartbeat() | Heartbeat")
        chatengine_log.debug("handle_poller_heartbeat() | Passed participants: %s", f"[\"{'\", \"'.join([p.name for p in participants])}\"]")
        chatengine_log.debug("handle_poller_heartbeat() | Current participants: %s", f"[\"{'\", \"'.join([p.name for p in self._participants])}\"]")

        if [p.id for p in participants] != [p.id for p in self._participants]:
            self._participants = participants
            chatengine_log.info("ChatEngine._participants updated")
            self.event_handler.notify('CHATENGINE_PARTICIPANT_UPDATE_PAYLOAD_EVENT',
                                      [user.name for user in self._participants]
                                      )


    @property
    def user(self):
        chatengine_log.info("Access to object ChatEngine.user")
        if isinstance(self._user, User):
            return self._user
        else:
            raise TypeError()


    @user.setter
    def user(self, user:User):
        chatengine_log.info("Attempt to set ChatEngine user to %s - %s", user.name, user.id)
        if isinstance(user, User):
            self._user: User = user
            chatengine_log.info("Success to set ChatEngine user")
        else:
            chatengine_log.error("Failed to set ChatEngine user: TypeError raised. Details: Type of user parameter %s", type(user).__name__)
            raise TypeError()



    @property
    def chatroom(self):
        return self._chatroom


    @chatroom.setter
    def chatroom(self, chatroom):
        if isinstance(chatroom, str):
            self._chatroom = chatroom
        else:
            raise TypeError()

    async def send_message(self, chatroom_id, message):
        users:list[User] = await self.net.get_chatroom_uparticipants(chatroom_id)
        remote_users = [user for user in users if user.id != self.user.id]
        if remote_users == []:
            return

        for user in remote_users:
            await send_message(user.endpoint_address, user.endpoint_port, message)
