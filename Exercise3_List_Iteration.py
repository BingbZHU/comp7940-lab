# Define the target list
l = [52633, 8137, 1024, 999]

# Iterate through each number in the list
for num in l:
    # Initialize an empty list to store the factors of the current number
    factors = []
    # Iterate through all integers from 1 to the current number (inclusive)
    for i in range(1, num + 1):
        # If num is divisible by i (remainder is 0), then i is a factor
        if num % i == 0:
            factors.append(i)
    # Output the result with clear formatting
    print(f"Factors of {num}: {factors}")