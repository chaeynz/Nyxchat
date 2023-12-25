# pylint: disable=redefined-outer-name, missing-docstring
import pytest
import asyncio
import threading

from modules.connection_handler import ConnectionHandler
from modules.event_handler import EventHandler

@pytest.fixture
def connection_handler():
    return ConnectionHandler(port=1337)

@pytest.fixture
def event_handler():
    return EventHandler()

def test_syn_send_and_receive(connection_handler, event_handler):
    message = "Test"
    response = None

    def callback(message):
        nonlocal response
        response = message

    event_handler.subscribe('message_received', callback=callback)

    listen_thread = threading.Thread(target=connection_handler.syn_listen, args=(event_handler,))
    listen_thread.daemon = True
    listen_thread.start()

    connection_handler.syn_send(data=message, address='127.0.0.1')

    assert response == message

@pytest.mark.asyncio
async def test_send_and_receive(connection_handler, event_handler):
    message = "Test"
    response = None

    def callback(message):
        nonlocal response
        response = message

    event_handler.subscribe('message_received', callback=callback)

    await connection_handler.listen()
    await connection_handler.send(data=message, address='127.0.0.1')

    assert response == message
