import secrets
import os
import time
from hashlib import sha256
from garytree import makeTree, data_parse

class Block:
    def __init__(self, blockchain, filename, bad_block):
        data = data_parse(filename)
        
        if bad_block:
            self.header = self.build_bad_block_header(blockchain, data)
            print("Bad block created, filename:", filename)
        else:
            self.header = self.build_header(blockchain, data)
            
        self.ledger = data       
        
    class Header:
        def __init__(self, header, root, timestamp, diff, nonce):
            self.hash_header = header
            self.hash_root = root
            self.timestamp = timestamp
            self.diff_target = diff
            self.nonce = nonce
            
    def build_bad_block_header(self, blockchain, data):
        random = (secrets.randbelow(100) + 1)
        
        if len(blockchain) == 0 :
            if random <= 33: # bad prev hash header
                hash_header = '0'*64
                print('bad previous hash header - ', end='')
            else :
                hash_header = 0
            
        else :
            if random <= 33 : # bad prev hash header
                hash_header = 0
                print('bad previous hash header - ', end='')
            else :
                prev = blockchain[-1].header
                hash_header = hash_string(str(prev.hash_header) + prev.hash_root + str(prev.timestamp) + prev.diff_target + str(prev.nonce))
        
        if random > 33 and random <= 66 : # bad merkle root
            hash_root = secrets.token_hex(32) # random 64 char hex string
            print('bad merkle root - ', end='')
        else :
            hash_root = makeTree(data)
            
        if random > 66 : # bad timestamp
            timestamp = 0
            print('bad timestamp - ', end='')
        else :
            timestamp = int(time.time())
            
        diff_target = "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        nonce = secrets.randbits(256)
        return Block.Header(hash_header, hash_root, timestamp, diff_target, nonce)
    
    
    def build_header(self, blockchain, data):
        
        if len(blockchain) == 0 :
            hash_header = 0
            
        else :
            prev = blockchain[-1].header
            hash_header = hash_string(str(prev.hash_header) + prev.hash_root + str(prev.timestamp) + prev.diff_target + str(prev.nonce))
            
        hash_root = makeTree(data)
        timestamp = int(time.time())
        diff_target = "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        nonce = find_nonce(diff_target,hash_root)
        return Block.Header(hash_header, hash_root, timestamp, diff_target, nonce)

      
# this assumes big endian when converting the bytes into int, not sure if that's right bc i'm pretty sure that sunlabs is little endian
def find_nonce(difficulty, root):
    # turns root hex string to bytes
    root = bytes.fromhex(root)
    # turns difficulty hex string to an unsigned int
    difficulty = int.from_bytes(bytes.fromhex(difficulty), "big")

    while True:
        # gets a uniformly random number with 256 bits and converts to bytes
        nonce = secrets.randbits(256)
        nonce_bytes = nonce.to_bytes(32, "big")

        # gets the raw byte hashed value of root (as bytes) plus nonce (as bytes)
        holder = sha256(root + nonce_bytes).digest()

        # if this value cast to an int is less than our target, return the nonce
        if int.from_bytes(holder, "big") <= difficulty:
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
    difficulty = int.from_bytes(bytes.fromhex(header.diff_target), "big")
    if difficulty <= 0 or difficulty > ((2 ** 256) - 1):
        return False
    if not isinstance(header.nonce, int) or header.nonce < 0:
        return False
    return True


# Function to serialize the block to a file
def serialize_block(block, file, full_print):
    if (full_print =="y"):
        result = "BEGIN BLOCK\n"
        result += "BEGIN HEADER\n"
        result += "Hash of previous header: " + str(block.header.hash_header) + "\n"
        result += "Merkle root: " + block.header.hash_root + "\n"
        result += "Timestamp: " + str(block.header.timestamp) + "\n"
        result += "Difficulty target: " + block.header.diff_target + "\n"
        result += "Nonce: " + str(block.header.nonce) + "\n"
        result += "END HEADER" + "\n"
        for accounts in block.ledger:
            result += accounts[0] +" "+ accounts[1] + "\n"
        result += "END BLOCK\n"
    else:
        result = "BEGIN BLOCK\n"
        result += "BEGIN HEADER\n"
        result += "Hash of previous header: " + str(block.header.hash_header) + "\n"
        result += "Merkle root: " + block.header.hash_root + "\n"
        result += "Timestamp: " + str(block.header.timestamp) + "\n"
        result += "Difficulty target: " + block.header.diff_target + "\n"
        result += "Nonce: " + str(block.header.nonce) + "\n"
        result += "END HEADER" + "\n"
        result += "END BLOCK\n"
    try:
        file = file.split(".txt")[0] + ".block.out"
        with open(file, "w") as f:
            f.write(result)

        #write to complete output
        write_complete_output(result, "data/complete.block.out")
    except Exception as e:
        print(f"An Unexpected error occurred: {e}")
        exit(1)


# Function to write all output to single file
def write_complete_output(content, output_file):

    #if file exits, decide whether to write or to append
    if os.path.exists(output_file):
        mode = 'a' #append to the existing file
    else:
        mode = 'w' #create a new file

    #write content to output_file
    with open(output_file, mode) as dst:
        dst.write(content)
    

# function to get the files list
def get_files():
    filename = input("Please enter all textfiles you wish to use separated by a space\n").strip()
    files = filename.split(" ")
    while not valid_files(files):
        filename = input("Please enter valid files you wish to use separated by a space\n").strip()
        files = filename.split(" ")
    return files


# Function to validate the input files
def valid_files(files):
    for file in files:
        try:
            if not os.path.isfile(file):
                print(f"File '{file}' does not exist.")
                return False
        except Exception as e:
            print(f"An Unexpected error occurred: {e}")
            return False
    return True

# Function to get print preference
def get_print_preference():
    full_print = input("Do you want to print the full ledger (y/n)?: ").strip().lower()
    while full_print != "y" and full_print != "n":
        full_print = input("Invalid input. Do you want to print the full ledger (y/n)?: ").strip().lower()
    return full_print


if __name__ == "__main__":

    #clearing existing data if file exists only on initial run through
    complete_output = "data/complete.block.out"

    if(os.path.isfile(complete_output)):
        file = open(complete_output,'w')
        file.close()
    
    blockchain = []
    
    files = get_files()

    full_print = get_print_preference()
        
    for filename in files:
        bad_block = (secrets.randbelow(100) + 1) <= 10 # 10% chance of being a bad block
        new_block = Block(blockchain, filename, bad_block)
        
        if validate_header(new_block.header) :
            blockchain.append(new_block)
            serialize_block(new_block, filename, full_print)
        else :
            del new_block

