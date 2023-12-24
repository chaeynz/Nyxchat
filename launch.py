# pylint: disable=missing-docstring, line-too-long
from modules.user import User
from modules.message import Message
from modules.network_engine import NetworkEngine
from modules.event_handler import EventHandler

def print_message(message):
    print(f"Message received: {message}")

def send_message(network_engine:NetworkEngine, user:User):
    message = Message(content=input("Message: "), author=user, recipient=User(user_id=input("Recipient ID: ")))
    network_engine.send_message(message)

def receive(network_engine:NetworkEngine, event_handler:EventHandler):
    event_handler.subscribe('message_received', print_message)
    network_engine.connection_handler.syn_listen(event_handler=event_handler)

def prompt_user(network_engine:NetworkEngine, event_handler:EventHandler, user:User):
    try:
        choice = int(input("""\t1. Send Message
        \t2. Receive Message"""))
        if choice == 1:
            send_message(network_engine=network_engine, user=user)
        elif choice == 2:
            receive(network_engine=network_engine, event_handler=event_handler)

    except ValueError:
        print("Please enter a valid choice!")
        return prompt_user(network_engine=network_engine, event_handler=event_handler, user=user)

def main():
    print("Welcome!\n")

    # Start network engine
    network_engine = NetworkEngine()

    # Start event handler
    event_handler = EventHandler()

    # Create User
    user = User()
    print(f"Current user ID: {str(user.id)}")

    # Let the user choose an option
    prompt_user(network_engine=network_engine, event_handler=event_handler, user=user)


if __name__ == "__main__":
    main()
