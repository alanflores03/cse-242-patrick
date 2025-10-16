from garytree import getTree, data_parse, makeTree
from blocks import Block, validate_header, serialize_block, get_files, get_print_preference, hash_string
import tempfile
import os
from math import log, ceil
import time
import secrets
# from collections import deque

# Function to take a block as input and return a boolean indicating if it is valid
def validation_block(block, current_time, previous_timestamp=None, previous_block=None):
    
    if not previous_block: # if genesis block
        
        data = get_account_data(block)
        root = makeTree(data) # returns hashed root

        # check merkle root
        if root != block.header.hash_root :
            return (False, 'Bad Merkle root') # if they are not the same
        
        # check timestamp
        if block.header.timestamp > current_time + 1 :
            return (False, 'Timestamp in future')
        
        # check previous header
        if block.header.hash_header != 0 :
            return (False, 'Previous header hash invalid') # means found invalid match of hashed headers


    else :
                
        data = get_account_data(block)
        root = makeTree(data) # returns hashed root

        if root != block.header.hash_root :
            return (False, 'Bad Merkle root') # if they are not the same
        
        # check timestamp
        if block.header.timestamp > current_time + 1 :
            return (False, 'Timestamp in future')
        elif block.header.timestamp < previous_timestamp :
            return (False, 'Timestamp less than previous block')

        # Instead of a hard coded value, in the future we may need to check against some global variable
        if block.header.diff_target != "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff":
            return (False, 'Incorrect difficulty target')

        # Reused code from find_nonce in blocks.py
        nonce_bytes = block.header.nonce.to_bytes(32, "big")
        holder = sha256(block.header.hash_root + nonce_bytes).digest()
        if int.from_bytes(holder, "big") > difficulty:
            return (False, 'Invalid nonce')
    
    return (True, None) # if all checks passed
        


# Function to valid a blockchain, returns true if chain is valid, false otherwise
def validation_chain(blockchain):

    # if empty chain
    if not blockchain:
        return (False, 0, 'No blockchain')
    
    current_time = int(time.time())
    
    # Checking genisis block outside of loop because no previous root
    genesis_block_validation = validation_block(blockchain[0], current_time)
    
    if not genesis_block_validation[0] :
        return (False, 0, genesis_block_validation[1])
  
    previous_timestamp = blockchain[0].header.timestamp
    previous_block = blockchain[0]    
    
    # Validate remainder of the chain
    for i in range(1, len(blockchain)) :
        block = blockchain[i]
        block_validation = validation_block(block, current_time, previous_timestamp, previous_block)
        
        #validating each block
        if not block_validation[0] :
            return (False, i, block_validation[1])
        
    
        previous_timestamp = block.header.timestamp
        previous_block = block
    
    return (True, None, None) # if entire chain matches expectations

# Function to get the account data from the block as a list to be passed into makeTree 
def get_account_data(block):
    accounts = []
    for account in block.ledger:
        info = account[0] +" "+ account[1]
        accounts.append(info)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as file:
        file.write("\n".join(accounts))
        filename = file.name
    
    try:
        data = data_parse(filename)
    finally:
        #take care of temp file
        os.unlink(filename)

    return data

# given an account string and a blockchain, either return the balance of the account or that the account doesn't exist in the blockchain
def balance(account, blockchain):
    tf, pom, node = proofOfMembership(account, blockchain)
    if tf:
        return node.data[1], pom
    return False

# iterates through each block in the blockchain backwards
# checks
def proofOfMembership(account, blockchain):
    output = []

    for block in reversed(blockchain):
        for i in range(len(block.ledger)):
            if account == block.ledger[i][0]:
                node = getTree(block.ledger)

                # stack of nodes
                nodes = []
                nodes.append(node)
                # log_2 of the number of leafs 
                level = ceil(log(len(block.ledger), 2)) + 1

                # lower end of range when checking where i is
                lower = 0
                
                # stops before the leaf nodes because the leafs have no left or right child
                while level > 1:
                    # if we are the second lowest level, check if the account node is a left or right child
                    if level == 2:
                        # if left child, check if sibling exists before adding
                        # we add node.left last because we want the relevant account node to be the last thing appended
                        if i % 2 == 0:
                            if node.right is not None:
                                nodes.append(node.right)
                            nodes.append(node.left)
                            node = node.left
                        # if it is a right child, no need for any checking and just append both
                        else:
                            nodes.append(node.left)
                            nodes.append(node.right)
                            node = node.right
                    # append both childs of the current node
                    else:
                        # if i is a decendent of the left node, we first add right node (if it exists) then the left and reset node to the left node
                        if i < (lower + 2 ** (level - 2)):
                            if node.right is not None:
                                nodes.append(node.right)
                            nodes.append(node.left)

                            node = node.left
                        # if i is a decendent of the right node, first append the left node and then the right before resetting node to the right node
                        else:
                            lower += 2 ** (level - 2)
                            nodes.append(node.left)
                            nodes.append(node.right)
                            
                            node = node.right
                    
                    level -= 1

                output.append(nodes.pop().data[2])
                holder = nodes.pop()
                # if this is true, there is a sibling to the leaf node which we will add
                if isinstance(holder.data, list):
                    output.append(holder.data[2])
                # if false, holder is the parent to our account node so we just add data
                else:
                    output.append(holder.data)
                    
                while nodes:
                    output.append(nodes.pop().data)
                
                # if len(output) is even, the acct was a left child and there was no right child
                # else, we don't know if it's left or right 
                return True, output, node

    return False, output, None

def get_failure_percentage():
    while True:
        try:
            percent_bad = int(input("Enter the percentage of bad blocks (0-100): ").strip())
            if 0 <= percent_bad <= 100:
                return percent_bad
            else:
                print("Percentage must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter an integer between 0 and 100.")
            
if __name__ == "__main__":
    blockchain = []
    
    files = get_files()
    
    percent_bad = get_failure_percentage()

    full_print = get_print_preference()
        
    for filename in files:
        bad_block = (secrets.randbelow(100) + 1) <= percent_bad
        new_block = Block(blockchain, filename, bad_block)
        
        if validate_header(new_block.header) :
            blockchain.append(new_block)
            serialize_block(new_block, filename, full_print)
        else :
            del new_block

    print('Blockchain validation: \n', 'Valid' if validation_chain(blockchain)[0] else f"Invalid : {validation_chain(blockchain)[2]} at block {validation_chain(blockchain)[1]}")
    print(balance("f294de1165d00fe497bbf89ff86aa5988239718c", blockchain))
    