# pylint:disable=missing-docstring
import curses
import asyncio

from modules.chatui import ChatUI
from modules.event_handler import EventHandler

from modules.network_engine import NetworkEngine
from modules.chat_engine import ChatEngine

def prompt_new_chatroom():
    print("Create a new Chatroom")
    return input(" > ")


def prompt_menu(selection):
    def draw_menu(stdscr, selected_row_idx):
        stdscr.clear()
        for idx, chatroom in enumerate(selection):
            if idx == selected_row_idx:
                stdscr.addstr(f"> {chatroom}\n", curses.color_pair(1) | curses.A_BOLD)  # Highlight selected item
            else:
                stdscr.addstr(f"  {chatroom}\n", curses.color_pair(2))  # Regular item
        stdscr.refresh()

    def menu(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Selected item: Green on Black
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Regular items: Cyan on Black
        curses.curs_set(0)  # Hide the cursor

        current_row = 0
        draw_menu(stdscr, current_row)

        while True:
            key = stdscr.getch()
            if key == curses.KEY_DOWN:
                current_row = (current_row + 1) % len(selection)
            elif key == curses.KEY_UP:
                current_row = (current_row - 1) % len(selection)
            elif key == 10:  # Enter key
                return selection[current_row]
            elif key == 27:  # ESC key
                return None
            draw_menu(stdscr, current_row)

    return curses.wrapper(menu)

async def send_message(chat: ChatEngine, chatroom_id, message):
    await chat.send_message(chatroom_id, message)

async def display_interactive_chat(username, chatroom_id):
    event_handler = EventHandler()
    chat = ChatEngine()

    def main(stdscr):
        stdscr.clear()
        ui = ChatUI(stdscr)
        ui.userlist.append(username)

        event_handler.subscribe('CHATENGINE_PARTICIPANT_UPDATE_PAYLOAD_EVENT', ui.set_userlist)
        event_handler.subscribe('CHAT_MSG_RCV_PAYLOAD_EVENT', ui.chatbuffer_add)


        ui.redraw_userlist()
        user_input = ""
        while user_input.lower() != "/quit":
            user_input = ui.wait_input(" > ")
            event_handler.notify('')
            ui.chatbuffer_add(user_input)
            

    return curses.wrapper(main)
