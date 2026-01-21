# Find all the factors of x using a loop and the modulus operator (%)
# % means to find the remainder, for example 10 % 2 = 0; 10 % 3 = 1
x = 52633
# Initialize the factor list and add 1 first (the smallest factor of all positive integers)
factors = [1]

# Loop to check all numbers between 2 and x-1 to see if they are factors of x
for i in range(2, x):
    # Core judgment: If the remainder of x divided by i is 0, it means i divides x exactly, so i is a factor of x
    if x % i == 0:
        factors.append(i)

# Finally, add x itself (the largest factor of all positive integers)
factors.append(x)

# Output the result
print(f"The factors of {x} are: {factors}")