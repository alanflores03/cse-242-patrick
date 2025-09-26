import secrets
from hashlib import sha256

class Block:
    def __init__(self):
        self.ledger = None
        self.header = None

    class Header:
        def __init__(self, hash_header, hash_root, timestamp, diff_target, nonce):
            self.hash_header = hash_header
            self.hash_root = hash_root
            self.timestamp = timestamp
            self.diff_target = "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            self.nonce = nonce



def find_nonce(difficulty, root):
    # turns root hex string to bytes
    r = bytes.fromhex(root)
    # turns difficulty hex string to an unsigned int
    d = int.from_bytes(bytes.fromhex(difficulty), "big")

    while True:
        # gets a uniformly random number with 256 bits and converts to bytes
        nonce = secrets.randbits(256)
        nonce_bytes = nonce.to_bytes(32, "big")

        # gets the raw byte hashed value of root (as bytes) plus nonce (as bytes)
        holder = sha256(r + nonce_bytes).digest()

        # if this value cast to an int is less than our target, return the nonce
        if int.from_bytes(holder, "big") <= d:
            return nonce
        


def hash_string(content):
    hashed = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return hashed
