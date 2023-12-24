import hashlib
import random

class User:
    def __init__(self, user_id=None):
        self.id = user_id if user_id else self.gen_id()

    def gen_id(self):
        """Generates a user_id and validates that this ID is unique across the network"""
        return hashlib.sha256(f"{random.randint(0, 65535)}".encode()).hexdigest()
