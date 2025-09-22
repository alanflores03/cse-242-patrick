from hashlib import sha256

#Binary tree implementation taken from W3Schools
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def makeTree (my_list):
    leafs = []
    nodes = []

    #makes all of the leaf nodes and adds to an array
    for i in range(len(my_list)):
        globals()['node' + str(i)] = TreeNode(my_list[i])
        leafs.append(globals()['node' + str(i)])

    for i in range(len(leafs) / 2):
        #this only works for first layer of parent nodes
        globals()['node' + str(i * 2) + str(i * 2 + 1)] = TreeNode(sha256(leafs[i * 2].data[2] + leafs[i * 2 + 1].data[2]).hexdigest)
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
                globals()['node' + str(i * counter) + str((i + 1) * counter - 1)] = TreeNode(sha256(leafs[i * 2].data + leafs[i * 2 + 1].data).hexdigest)
                globals()['node' + str(i * counter) + str((i + 1) * counter - 1)].left = leafs[i * 2]
                globals()['node' + str(i * counter) + str((i + 1) * counter - 1)].right = leafs[i * 2 + 1]                
                nodes.append(globals()['node' + str(i * 4) + str((i + 1) * counter - 1)])
        
        counter = 2 * counter       
        leafs = nodes
        nodes = []
        
        if len(leafs) == 1:
            break
    
    return leafs[0].data

