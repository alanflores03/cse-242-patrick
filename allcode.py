####### datacreation.py #######

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
    filename = input("Enter the output file name (e.g., testdata.txt): ").strip()
    if not filename:
        print("Invalid file name.")
        return
    
    # Prompt for number of test entries
    try:
        num_entries = int(input("Enter the number of entries to generate: ").strip())
        if num_entries <= 0:
            raise ValueError
    except ValueError:
        print("Invalid number of entries.")
        return
    
    # Generate test data
    test_data = generate_test_data(num_entries)
    
    # Write to file
    with open(filename, "w") as f:
        for addr, balance in test_data:
            f.write(f"{addr} {balance}\n")
    
    print(f"Test data successfully written to {filename}")

if __name__ == "__main__":
    main()











####### garytree.py #######
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
                if (i + 1) * counter - 1 > max_node:
                    nodes.append(TreeNode(sha256((leafs[i * 2].data[2] + leafs[i * 2 + 1].data[2]).encode('utf-8')).hexdigest()))
                    nodes[-1].left = leafs[i * 2]
                    nodes[-1].right = leafs[i * 2 + 1]

                else:
                    nodes.append(TreeNode(sha256((leafs[i * 2].data[2] + leafs[i * 2 + 1].data[2]).encode('utf-8')).hexdigest()))
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