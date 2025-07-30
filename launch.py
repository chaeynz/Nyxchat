# pylint: disable=missing-docstring, line-too-long
import asyncio
import random
import json

from modules.cliux import prompt_menu, prompt_new_chatroom, display_interactive_chat
from modules.user import User
from modules.connection_handler import run_server_in_background
from modules.event_handler import EventHandler
from modules.network_engine import NetworkEngine
from modules.chat_engine import ChatEngine


event_handler = EventHandler()
net = NetworkEngine()

ME      = '127.0.0.1'
MY_PORT = random.randint(1330,1340)

try:
    with open('config/bootstrap_nodes.json', 'r', encoding='utf-8') as f:
        BOOTSTRAP_NODES = [(node['address'].split(':')[0], int(node['address'].split(':')[1])) for node in json.load(f)]
except FileNotFoundError:
    BOOTSTRAP_NODES = []
except json.decoder.JSONDecodeError:
    BOOTSTRAP_NODES = []


async def main():
    name = input("username: ")
    user = User(name=name)

    sel = prompt_menu([user.id[:15], "New User"])
    if sel == "New User":
        user._generate_new_keys()
        user.save_user()

    chat = ChatEngine()
    chat.user = user

    await net.bootstrap(BOOTSTRAP_NODES)
    await net.update_location(user, ME, MY_PORT)

    sel_chatroom = prompt_menu(await net.get_chatrooms() + ["Create a new Chatroom"])

    if sel_chatroom == "Create a new Chatroom":
        sel_chatroom = prompt_new_chatroom()
    await net.join_chatroom(user, sel_chatroom)


    print(f"My Endpoint: {ME}:{MY_PORT}")
    print(f"In Chatroom: {sel_chatroom}")

    try:
        run_server_in_background(ME, MY_PORT)
    except OSError:
        raise OSError

    await net.start_polling_participants(sel_chatroom)

    try:
        await display_interactive_chat(user.name, sel_chatroom)
    except KeyboardInterrupt:
        pass
    finally:
        print("I'm alive")
        await net.leave_chatroom(user, sel_chatroom)
        await net.kill_location(user)
        net.terminate()

if __name__ == '__main__':
    asyncio.run(main())
