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