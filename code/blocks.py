
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
    