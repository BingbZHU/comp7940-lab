def print_factor(x):
    # Handle the special case where x is 0: 0 has no factors
    if x == 0:
        print("0 has no factors")
        return
    
    # Handle negative numbers: factors are typically discussed for positive integers, so take the absolute value
    num = abs(x)
    
    # Print a prompt to clarify which number's factors are being output
    print(f"All positive factors of {x}:")
    
    # Iterate through all integers from 1 to num (inclusive) to find factors
    for i in range(1, num + 1):
        # Modulo operation: if the remainder is 0, i is a factor of num
        if num % i == 0:
            # Print the found factor, end=" " to display all factors on the same line separated by spaces
            print(i, end=" ")
    
    # Print a new line to make the output format cleaner
    print()

# Test examples (to verify the function functionality)
if __name__ == "__main__":
    print_factor(12)   # Output: All positive factors of 12: 1 2 3 4 6 12 
    print_factor(-8)   # Output: All positive factors of -8: 1 2 4 8 
    print_factor(7)    # Output: All positive factors of 7: 1 7 
    print_factor(0)    # Output: 0 has no factors