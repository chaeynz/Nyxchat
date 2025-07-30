import asyncio
import threading
import socket

from modules.event_handler import EventHandler

event_handler = EventHandler()

def handle_client(client_socket):
    """Handles communication with a single client."""
    with client_socket:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            event_handler.notify('CHAT_MSG_RCV_PAYLOAD_EVENT', message.decode('utf-8'))


def start_listener(ip, port):
    """Starts a TCP listener to accept incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ip, port))
        server_socket.listen(5)

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.daemon = True  # Ensures thread will close when main program exits
            client_thread.start()


def run_server_in_background(ip, port):
    """Runs the start_listener function in a separate thread."""
    listener_thread = threading.Thread(target=start_listener, args=(ip, port))
    listener_thread.daemon = True  # Ensures thread will close when main program exits
    listener_thread.start()


async def send_message(ip, port, message):
    reader, writer = await asyncio.open_connection(ip, port)

    try:
        writer.write(message.encode('utf-8'))
        await writer.drain()
        print(f"Message sent to {ip}:{port}")
    except Exception as e:
        print(f"Failed to send message: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

# Example usage
async def main():
    recipient_ip = '192.168.1.2'  # Replace with the recipient's IP address
    recipient_port = 12345         # Replace with the recipient's port number
    message = 'Hello, this is a test message!'

    await send_message(recipient_ip, recipient_port, message)

if __name__ == '__main__':
    asyncio.run(main())
