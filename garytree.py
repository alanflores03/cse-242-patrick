from hashlib import sha256

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

test()