class EventHandler:
    _self = None

    def __init__(self):
        self.callbacks:dict(list) = {"message_received": []}

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def subscribe(self, event, callback):
        self.callbacks[event].append(callback)

    def notify(self, event, arg):
        for callback in self.callbacks[event]:
            if arg:
                callback(arg)
            else:
                callback()
