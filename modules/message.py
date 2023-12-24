# pylint: disable=missing-docstring
from modules.user import User

class Message():
    def __init__(self, author:User, recipient:User, content):
        self.author_id = author.id
        self.recipient_id = recipient.id
        self.content = content

    def __str__(self):
        return f"{self.author_id},{self.content}"
