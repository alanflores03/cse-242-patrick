from hashlib import sha256


#Binary tree implementation taken from W3Schools
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# Function to parse data from a data file, parse the data, and return as a list of lists
# The inner lists contains the entries as [address, balance, hash(address)], with the outer lists storing these entries
# Returns a the data of the file as a list of lists
def data_parse(filename):
    # List to store the entries
    data_lists = []
    try:
        with open(filename, "r", encoding='utf-8') as file:

            # Reading each entry in the file, hashing the address, and storing it all in a list
            for line in file:
                entry = line.strip().split(' ')
                hashed_address = sha256((entry[0]).encode('utf-8')).hexdigest()
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

    #makes all of the leaf nodes and adds to an array
    for i in range(len(my_list)):
        globals()['node' + str(i)] = TreeNode(my_list[i])
        leafs.append(globals()['node' + str(i)])

    for i in range(int(len(leafs) / 2)):
        #this only works for first layer of parent nodes
        globals()['node' + str(i * 2) + str(i * 2 + 1)] = TreeNode(sha256((leafs[i * 2].data[2] + leafs[i * 2 + 1].data[2]).encode('utf-8')).hexdigest())

        globals()['node' + str(i * 2) + str(i * 2 + 1)].left = leafs[i * 2]
        globals()['node' + str(i * 2) + str(i * 2 + 1)].right = leafs[i * 2 + 1]
        nodes.append(globals()['node' + str(i * 2) + str(i * 2 + 1)])
        
    leafs = nodes
    nodes = []

    counter = 4  #counter to fix naming convention
    
    while True :
        for i in range(int(len(leafs) / 2)):
            
            # if odd number of leafs, make last node only have left child
            if i == int(len(leafs) / 2) - 1 and len(leafs) % 2 != 0 :
                globals()['node' + str(i * counter) + str(i * counter + counter/2 - 1)] = TreeNode(leafs[i * 2].data)
                globals()['node' + str(i * counter) + str(i * counter + counter/2 - 1)].left = leafs[i * 2]              
                nodes.append(globals()['node' + str(i * counter) + str(i * counter + counter/2 - 1)])
                
            else :
                globals()['node' + str(i * counter) + str((i + 1) * counter - 1)] = TreeNode(sha256((leafs[i * 2].data[2] + leafs[i * 2 + 1].data[2]).encode('utf-8')).hexdigest())
                globals()['node' + str(i * counter) + str((i + 1) * counter - 1)].left = leafs[i * 2]
                globals()['node' + str(i * counter) + str((i + 1) * counter - 1)].right = leafs[i * 2 + 1]                
                nodes.append(globals()['node' + str(i * 4) + str((i + 1) * counter - 1)])
        
        counter = 2 * counter       
        leafs = nodes
        nodes = []
        
        if len(leafs) == 1:
            break
    
    return leafs[0].data




# Function to test the data: WILL NOT BE IN THE FINAL SUBMISSION JUST FOR HOW YOU CAN SEE THE OUTPUT
# Just call test() under here to see the output of the data parsing
# Before running this, make sure you create the data file using datacreation.py. Creating 5 entries should be good enough for viewing the output, 
# but definitely create more when we are testing the actual tree 
def test():
    file = get_file()
    data = data_parse(file)
    # again, the data is outputted as follows: [address, balance, hash(address)]
    for i in data:
        print(i)  # For testing purposes, print the parsed data
        print()
    tree = makeTree(data)
    print("The tree is: " + tree)
test()