# pylint: disable = missing-docstring
import os
import logging
import inspect

LOG_PATH = 'log/'
EVENTHANDLER_LOG_PATH = f'{LOG_PATH}eventhandler.log'

os.makedirs(LOG_PATH, exist_ok=True)

handler = logging.FileHandler(EVENTHANDLER_LOG_PATH)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
eventhandler_log = logging.getLogger('eventhandler')
eventhandler_log.addHandler(handler)
eventhandler_log.setLevel(logging.DEBUG)

class EventHandler:
    _self = None
    _init = False

    def __init__(self):
        if not EventHandler._init:
            self._callbacks:dict(list) = {}
            EventHandler._init = True

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def subscribe(self, event: str, callback):
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)
        eventhandler_log.info('%s subscribed to %s', callback.__name__, event)

    def notify(self, event: str, *args, **kwargs):
        """Notify all subscribed callbacks for a given event with arguments."""
        who_called_me: str = inspect.currentframe().f_back.f_code.co_name

        eventhandler_log.info('%s notified %s', who_called_me, event) # Logs the function that calls notify()
        if event in self._callbacks:
            eventhandler_log.info('%s is available', event)
            for callback in self._callbacks[event]:
                try:
                    callback(*args, **kwargs)
                    eventhandler_log.info('Executed callback: %s', callback.__name__)
                    

                except Exception as e:
                    eventhandler_log.error('Error executing callback %s for event %s: %s', callback.__name__, event, e)
