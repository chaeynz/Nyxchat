# pylint: disable=no-member
import curses
import logging
import os
from curses import wrapper


import curses
from threading import Thread


LOG_PATH = 'log/'
CHATUI_LOG_PATH = f'{LOG_PATH}chatui.log'

os.makedirs(LOG_PATH, exist_ok=True)

handler = logging.FileHandler(CHATUI_LOG_PATH)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
chatui_log = logging.getLogger('chatui')
chatui_log.addHandler(handler)
chatui_log.setLevel(logging.DEBUG)


class ChatUI:

    _self = None

    def __init__(self, stdscr, userlist_width=50):
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, -1)
        self.stdscr = stdscr
        self.userlist: list[str] = []
        self.inputbuffer = ""
        self.linebuffer = []
        self.chatbuffer = []
        self.dht_info_content = "DHT Information Placeholder"
        self.user_input = None

        dht_info_height = 3
        userlist_height = (curses.LINES - 2) - dht_info_height - 2

        chatbuffer_hwyx = (curses.LINES - 2, curses.COLS - userlist_width - 1, 0, 0)
        dht_info_hwyx = (dht_info_height, userlist_width - 1, 1, curses.COLS - userlist_width)
        userlist_hwyx = (userlist_height, userlist_width - 1, dht_info_height + 2, curses.COLS - userlist_width)
        chatline_yx = (curses.LINES - 1, 0)

        self.win_chatbuffer = stdscr.derwin(*chatbuffer_hwyx)
        self.win_dht_info = stdscr.derwin(*dht_info_hwyx)
        self.win_userlist = stdscr.derwin(*userlist_hwyx)
        self.win_chatline = stdscr.derwin(*chatline_yx)

        stdscr.nodelay(True)  # Enable non-blocking mode
        self.redraw_ui()

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def set_userlist(self, userlist: list[str]):
        chatui_log.info('Userlist was set to: %s', repr(userlist))
        self.userlist: list[str] = userlist
        self.redraw_userlist()

    def resize(self):
        h, w = self.stdscr.getmaxyx()
        dht_info_height = 3
        userlist_height = h - dht_info_height - 3

        self.win_chatline.mvwin(h - 1, 0)
        self.win_chatline.resize(1, w)

        self.win_chatbuffer.resize(h - 2, w - self.win_userlist.getmaxyx()[1] - 1)
        self.win_dht_info.resize(dht_info_height, self.win_userlist.getmaxyx()[1])
        self.win_userlist.resize(userlist_height, self.win_userlist.getmaxyx()[1])

        self.linebuffer = []
        for msg in self.chatbuffer:
            self._linebuffer_add(msg)

        self.redraw_ui()

    def redraw_ui(self):
        h, w = self.stdscr.getmaxyx()
        chat_w = self.win_chatbuffer.getmaxyx()[1]
        self.stdscr.clear()
        self.stdscr.vline(0, chat_w, "|", h - 2)
        self.stdscr.hline(h - 2, 0, "-", w)

        self.stdscr.hline(0, chat_w, "-", w - chat_w)  # Top line
        self.stdscr.hline(3 + 1, chat_w, "-", w - chat_w)  # Bottom line

        self.stdscr.refresh()

        self.redraw_chatbuffer()
        self.redraw_dht_info()
        self.redraw_userlist()
        self.redraw_chatline()

    def redraw_dht_info(self):
        self.win_dht_info.clear()
        h, w = self.win_dht_info.getmaxyx()
        start_col = max(0, (w - len(self.dht_info_content)) // 2)
        self.win_dht_info.addstr(1, start_col, self.dht_info_content[:w])
        self.win_dht_info.refresh()

    def redraw_chatline(self):
        h, w = self.win_chatline.getmaxyx()
        self.win_chatline.clear()
        start = len(self.inputbuffer) - w + 1
        if start < 0:
            start = 0
        self.win_chatline.addstr(0, 0, self.inputbuffer[start:])
        self.win_chatline.refresh()

    def redraw_userlist(self):
        self.win_userlist.clear()
        h, w = self.win_userlist.getmaxyx()
        for i, name in enumerate(self.userlist):
            if i >= h:
                break
            start_col = max(0, (w - len(name)) // 2)
            self.win_userlist.addstr(i, start_col, name[:w])
        self.win_userlist.refresh()

    def redraw_chatbuffer(self):
        self.win_chatbuffer.clear()
        h, w = self.win_chatbuffer.getmaxyx()
        j = len(self.linebuffer) - h
        if j < 0:
            j = 0
        for i in range(min(h, len(self.linebuffer))):
            self.win_chatbuffer.addstr(i, 0, self.linebuffer[j])
            j += 1
        self.win_chatbuffer.refresh()

    def chatbuffer_add(self, msg):
        self.chatbuffer.append(msg)
        self._linebuffer_add(msg)
        self.redraw_chatbuffer()
        self.redraw_chatline()
        self.win_chatline.cursyncup()

    def _linebuffer_add(self, msg):
        h, w = self.stdscr.getmaxyx()
        u_h, u_w = self.win_userlist.getmaxyx()
        w = w - u_w - 2
        while len(msg) >= w:
            self.linebuffer.append(msg[:w])
            msg = msg[w:]
        if msg:
            self.linebuffer.append(msg)

    def prompt(self, msg):
        """Prompts the user for input and returns it"""
        self.inputbuffer = msg
        self.redraw_chatline()
        res = self.wait_input()
        res = res[len(msg):]
        return res

    def wait_input(self, prompt=""):
        """Non-blocking input handling"""
        self.inputbuffer = prompt
        self.redraw_chatline()
        self.win_chatline.cursyncup()
        last = -1
        while True:
            last = self.stdscr.getch()
            if last == ord('\n'):
                tmp = self.inputbuffer
                self.inputbuffer = ""
                self.redraw_chatline()
                self.win_chatline.cursyncup()
                return tmp[len(prompt):]
            elif last == curses.KEY_BACKSPACE or last == 127:
                if len(self.inputbuffer) > len(prompt):
                    self.inputbuffer = self.inputbuffer[:-1]
            elif last == curses.KEY_RESIZE:
                self.resize()
            elif 32 <= last <= 126:
                self.inputbuffer += chr(last)
            self.redraw_chatline()
            curses.napms(50)  # Small sleep to prevent high CPU usage



def main(stdscr):
    stdscr.clear()
    ui = ChatUI(stdscr)
    name = ui.wait_input("Username: ")
    ui.userlist.append(name)
    ui.redraw_userlist()
    inp = ""
    while inp != "/quit":
        inp = ui.wait_input()
        ui.chatbuffer_add(inp)

#wrapper(main)