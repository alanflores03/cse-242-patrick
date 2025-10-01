import secrets
import time
from hashlib import sha256
from garytree import makeTree, data_parse

class Block:
    def __init__(self, blockchain, filename):
        data = data_parse(filename)
        self.header = self.build_header(blockchain, data)
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
            prev = blockchain[-1].header
            hash_header = hash_string(str(prev.hash_header) + prev.hash_root + str(prev.timestamp) + prev.diff_target + str(prev.nonce))
            
        hash_root = makeTree(data)
        diff_target = "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        nonce = find_nonce(diff_target,hash_root)
        return Block.Header(hash_header, hash_root, diff_target, nonce)

      
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
    hashed = sha256(content.encode('utf-8')).hexdigest()
    return hashed

# This function validates the block header data and ensures it is filled out correctly.
# Returns true if valid, false if not. 
def validate_header(header):
    if header.hash_header != 0:
        if len(header.hash_header) != 64:
            return False
    if  len(header.hash_root) != 64:
        return False
    if header.timestamp < 0:
        return False
    d = int.from_bytes(bytes.fromhex(header.diff_target), "big")
    if d <= 0 or d > 2 ** 255 - 1:
        return False
    if not isinstance(header.nonce, int) or header.nonce < 0:
        return False
    return True

if __name__ == "__main__":
    
    blockchain = []
    
    filename = input("Please enter all textfiles you wish to use separated by a space\n").strip()
    files = filename.split(" ")
    # files = ["test.txt","test2.txt", "data/testdata.txt"]

    full_print = input("Do you want to print the full ledger (y/n)?: ").strip()

    while full_print != "y" and full_print != "n":
        full_print = input("Invalid input. Do you want to print the full ledger (y/n)?: ").strip()
        
    for filename in files:
        new_block = Block(blockchain, filename)
        
        if validate_header(new_block.header) :
            blockchain.append(new_block)
            out = filename.split(".txt")[0] + ".block.out"
            with open(out, "w") as file:
                if full_print == "y":
                    file.write("BEGIN BLOCK\n")
                    file.write("BEGIN HEADER\n")
                    file.write("Hash of previous header: " + str(new_block.header.hash_header) + "\n")
                    file.write("Merkle root: " + new_block.header.hash_root + "\n")
                    file.write("Timestamp: " + str(new_block.header.timestamp) + "\n")
                    file.write("Difficulty target: " + new_block.header.diff_target + "\n")
                    file.write("Nonce: " + str(new_block.header.nonce) + "\n")
                    file.write("END HEADER" + "\n")
                    for el in new_block.ledger:
                        file.write(el[0] +" "+ el[1] +" "+el[2] + "\n")
                    file.write("END BLOCK\n")
                else:
                    file.write("BEGIN BLOCK\n")
                    file.write("BEGIN HEADER\n")
                    file.write("Hash of previous header: " + str(new_block.header.hash_header) + "\n")
                    file.write("Merkle root: " + new_block.header.hash_root + "\n")
                    file.write("Timestamp: " + str(new_block.header.timestamp) + "\n")
                    file.write("Difficulty target: " + new_block.header.diff_target + "\n")
                    file.write("Nonce: " + str(new_block.header.nonce) + "\n")
                    file.write("END HEADER" + "\n")
                    file.write("END BLOCK\n")
        else :
            del new_block
