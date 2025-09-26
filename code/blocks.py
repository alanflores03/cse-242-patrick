
class header:
    def __init__(self, hash_header, hash_root, timestamp, diff_target, nonce):
        self.hash_header = hash_header
        self.hash_root = hash_root
        self.timestamp = timestamp
        self.diff_target = diff_target
        self.nonce = nonce

class block:
    