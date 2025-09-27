import secrets
import time
from hashlib import sha256
from garytree import makeTree, data_parse

class Block:
    def __init__(self, blockchain, filename):
        data = data_parse(filename)
        self.header = build_header(blockchain, data)
        self.ledger = data       
        
    class Header:
        def __init__(self, header, root, diff, nonce):
            self.hash_header = header
            self.hash_root = root
            self.timestamp = int(time.time())
            self.diff_target = diff
            self.nonce = nonce
    
    def build_header(self, blockchain, data):
        
        if len(blockchain) == 0 :
            hash_header = 0
            
        else :
            previous_header = blockchain[-1]
            hash_header = hash_string(previous_header)
            
        hash_root = makeTree(data)
        diff_target = "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        nonce = find_nonce(diff_target,hashroot)
        return Header(hash_header, hash_root, diff_target, nonce)

      
# this assumes big endian when converting the bytes into int, not sure if that's right bc i'm pretty sure that sunlabs is little endian
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

if __name__ == "__main__":
    
    blockchain = []
    files = []
    
    filename = "files.txt"
    
    try:
        with open(filename, "r", encoding='utf-8') as file:

            # Reading each entry in the file and storing it all in a list
            for line in file:
                entry = line.strip().split(' ')
                files.append(entry)
                
    except Exception as e:
        print(f"An Unexpected error occurred: {e}")
        exit(1)
        
    for filename in files:
        new_block = Block(blockchain, filename)
        
        if validate_header(new_block.header) :
            blockchain.append(new_block)
        
        else :
            del new_block
    