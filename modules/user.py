# pylint: disable=missing-docstring
import base64
import logging
import hashlib
import os
from kyber import Kyber1024

log = logging.getLogger(__name__)


CRYPTOSTOR_PATH = 'cryptostor/'
PRIVATE_KEY_FILE = f'{CRYPTOSTOR_PATH}my_kyber.key'
PUBLIC_KEY_FILE = f'{CRYPTOSTOR_PATH}my_kyber.pub'


def hash_key(key_bytes):
    """Compute SHA-256 hash of the given key bytes."""
    return hashlib.sha256(key_bytes).hexdigest()


class User:
    def __init__(self,
                 name = "",
                 id: str = None,
                 pk: bytes = None,
                 sk: bytes = None
                 ):

        self.name: str = name       # String
        self.id: str = id           # SHA256 Hash
        self.sk: bytes = sk         # Secret Key Bytes
        self.pk: bytes = pk         # Public Key Bytes
        self.endpoint_address = ''  # IP Address
        self.endpoint_port = 0      # Port

        if id is None:
            self.load_user()



    def load_user(self):
        """Load user data from files, generating new keys if necessary."""
        try:
            self._load_keys_from_files()
        except FileNotFoundError as e:
            log.info("One of the kyber files was missing, generating new user.\nDetails: %s", e)
            self._generate_new_keys()


    def _load_keys_from_files(self):
        """Load public and private keys from files."""
        os.makedirs(CRYPTOSTOR_PATH, exist_ok=True)
        with open(PUBLIC_KEY_FILE, 'r', encoding='utf-8') as f:
            self.pk = base64.b64decode(f.read().strip())
            self.id = hash_key(self.pk)

        with open(PRIVATE_KEY_FILE, 'r', encoding='utf-8') as f:
            self.sk = base64.b64decode(f.read().strip())


    def _generate_new_keys(self):
        """Generate a new public/private key pair and save them."""
        pk, sk = Kyber1024.keygen()
        self.pk = pk
        self.sk = sk
        self.id = hash_key(pk)
        print(f"user_id: {self.id}")
        self.save_user()


    def _generate_id_from_private_key(self, private_key):
        """Generate an ID from a private key."""
        # Assuming the ID can be derived from the private key, implement the logic if necessary
        return hash_key(private_key)


    def save_user(self):
        """Save the user's private and public keys to files."""
        with open(PRIVATE_KEY_FILE, 'w', encoding='utf-8') as f:
            f.write(base64.b64encode(self.sk).decode('utf-8'))

        with open(PUBLIC_KEY_FILE, 'w', encoding='utf-8') as f:
            f.write(base64.b64encode(self.pk).decode('utf-8'))


    def set_name(self, name):
        """Set the user's name."""
        self.name = name


if __name__ == '__main__':
    user = User(name="chaeynz")
