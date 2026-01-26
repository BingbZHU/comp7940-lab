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

# ------------------- Exercise 3: List Iteration -------------------
# Write a program to find all factors of the numbers in the list l
l = [52633, 8137, 1024, 999]

# Apply the print_factor function to each number in the list
for num in l:
    print_factor(num)