import hashlib
from modules.user import User
from modules.message import Message
from modules.network_engine import NetworkEngine
from modules.event_handler import EventHandler

def print_message(message):
    print(f"Message received: {message}")

def main():
    print("Welcome!")

    # Start network engine
    network_engine = NetworkEngine()

    # Start event handler and register callback for receiving messages
    event_handler = EventHandler()
    event_handler.subscribe("message_received", print_message)

    user = User()
    print(f"Current user ID: {str(user.id)}")
    message = Message(content=input("Message: "), author=user, recipient=User(user_id=input("Recipient ID: ")))
    network_engine.send_message(message)


if __name__ == "__main__":
    main()
