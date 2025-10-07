from hashlib import sha256
from garytree import getTree, data_parse, get_file
from blocks import Block, validate_header, serialize_block, get_files, get_print_preference
from math import log, ceil
# from collections import deque


# do balance and proof-of-membership

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

    print(balance("f294de1165d00fe497bbf89ff86aa5988239718c", blockchain))
    