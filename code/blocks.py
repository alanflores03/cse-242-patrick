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


# This function validates the block header data and ensures it is filled out correctly.
# Returns true if valid, false if not. 
def validate_header(header):
    if len(header.hash_header) != 64:
        return False
    if  len(header.hash_root) != 64:
        return False
    if header.timestamp < 0:
        return False
    if header.diff_target <= 0:
        return False
    if not isinstance(header.nonce, int) or header.nonce < 0:
        return False
    return True