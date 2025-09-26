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
            self.diff_target = diff_target
            self.nonce = nonce
    


def hash_string(content):
    hashed = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return hashed
