##################
## datacreation.py
##################

# PREFACE: WE ARE USING CHATGPT TO GENERATE THIS ENTIRE FILE TO USE DATA
import random
import string

def generate_hex_address(length=40):
    """Generate a random hex string of given length (0-9, a-f)."""
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))

def generate_test_data(num_entries=10, max_balance=10**7):
    """Generate a list of (address, balance) pairs."""
    addresses = set()
    while len(addresses) < num_entries:
        addresses.add(generate_hex_address())
    
    data = [(addr, random.randint(0, max_balance)) for addr in addresses]
    return sorted(data, key=lambda x: x[0])  # sort alphabetically by address

def main():
    # Prompt for file name
    filename = input("Enter the output file names without extension (e.g., testdata): ").strip()
    if not filename or '.' in filename:
        print("Invalid file name.")
        return
        
    # Prompt for number of data files
    try:
        num_files = int(input("Enter the number of files to generate: ").strip())
        if num_files <= 0:
            raise ValueError
    except ValueError:
        print("Invalid number of files.")
        return
    
    # Prompt for number of test entries
    try:
        num_entries = int(input("Enter the number of entries to generate: ").strip())
        if num_entries <= 0:
            raise ValueError
    except ValueError:
        print("Invalid number of entries.")
        return
    
    for i in range(num_files):
        
        # Generate test data
        test_data = generate_test_data(num_entries)
        
        data_filename = f"{filename}{i+1}.txt"
        
        # Write to datafile
        with open(data_filename, "w") as f:
            for addr, balance in test_data:
                f.write(f"{addr} {balance}\n")
               
        print(f"Test data successfully written to {data_filename}")
        
    with open(filename+'.txt', "w") as f:
        for i in range(num_files):
            f.write(f"{filename}{i+1}.txt ")

    print(f"All the prvious filenames are written to {filename}.txt")
    
if __name__ == "__main__":
    main()




#############
##garytree.py 
#############
from hashlib import sha256


#Binary tree implementation taken from W3Schools
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# Function to parse data from a data file line by line and return as a list of lists
# The inner lists contains the entries as [address, balance, hash(address+balance)], with the outer lists storing these entries
# Returns a the data of the file as a list of lists
def data_parse(filename):
    # List to store the entries
    data_lists = []
    try:
        with open(filename, "r", encoding='utf-8') as file:

            # Reading each entry in the file, hashing the address, and storing it all in a list
            for line in file:
                entry = line.strip().split(' ')
                hashed_address = sha256((entry[0]+entry[1]).encode('utf-8')).hexdigest()
                entry.append(hashed_address)

                # Adding entry to the data_lists
                data_lists.append(entry)
    except Exception as e:
        print(f"An Unexpected error occurred: {e}")
        exit(1)

    return data_lists


# Function to get the data file name from the user 
# Returns the file name as a string
def get_file():
    try:
        filename = input("Enter the data file name: ").strip()
        
        if not filename:
            print ("Please enter a non-empty file name")
            exit(2)
        return filename
    
    except Exception as e:
        print(f"An Unexpected error occurred: {e}")
        exit(1)
        
# Function to make the Merkle Tree
# my_list will be the list returned from get_file()
# Iterates through each layer of the Merkle tree, hashing and adding children
# Returns only the hash of the Merkle root
def makeTree (my_list):
    leafs = []
    nodes = []
    max_node = 0

    # naming convention is node_x,y where x is the left most related leaf node (child, grandchild etc.) and y is the right most related leaf node
    # leaf nodes are simply named node_#
    # counter used for naming purposes
    counter = 4

    # makes all of the leaf nodes and adds to an array
    for i in range(len(my_list)) :
        leafs.append(TreeNode(my_list[i]))

    for i in range(len(leafs) // 2) :
        # this only works for first layer of parent nodes
        nodes.append(TreeNode(sha256((leafs[i * 2].data[2] + leafs[i * 2 + 1].data[2]).encode('utf-8')).hexdigest()))
        nodes[-1].left = leafs[i * 2]
        nodes[-1].right = leafs[i * 2 + 1]
    
    # accounts for the single odd node left if it exists
    if len(leafs) % 2 != 0 :
        nodes.append(TreeNode((leafs[len(leafs) - 1].data[2])))

    max_node = len(leafs) - 1
    
    while True :

        leafs = nodes
        nodes = []
        
        for i in range((len(leafs) // 2) + 1) :
            
            # if odd number of nodes, make last node only have left child
            if i == ((len(leafs) // 2)) :
                if len(leafs) % 2 != 0 :
                    nodes.append(TreeNode(leafs[i * 2].data))
                    nodes[-1].left = leafs[i * 2]

                # if there is no odd node, we need to break and not go into else statement
                else :
                    break
                
            # normal case
            else :
                # checks when making right most node that we are numbering correctly with max node val we have and not the max possible value
                nodes.append(TreeNode(sha256((leafs[i * 2].data + leafs[i * 2 + 1].data).encode('utf-8')).hexdigest()))
                nodes[-1].left = leafs[i * 2]
                nodes[-1].right = leafs[i * 2 + 1]

        counter = 2 * counter       
        
        if len(leafs) == 1:
            break
    
    return leafs[0].data



if __name__ == "__main__":
    file = get_file()
    data = data_parse(file)
    tree = makeTree(data)
    print("The Merkle root is: " + tree)




#############
## blocks.py
#############

import secrets
import os
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
            result += accounts[0] +" "+ accounts[1] +" "+accounts[2] + "\n"
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
    except Exception as e:
        print(f"An Unexpected error occurred: {e}")
        exit(1)



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
    
    blockchain = []
    
    files = get_files()

    full_print = get_print_preference()
        
    for filename in files:
        new_block = Block(blockchain, filename)
        
        if validate_header(new_block.header) :
            blockchain.append(new_block)
            serialize_block(new_block, filename, full_print)
        else :
            del new_block

