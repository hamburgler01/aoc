import numpy as np

WIDTH = 25
HEIGHT = 6

def main():
    # Read input as a 1-D array of single numbers
    with open('input_01.txt') as input_file:
        nums = [int(i) for i in list(input_file.readline().strip())]

    # Reshape input into a 3-D array.
    z_dim = len(nums) // (WIDTH * HEIGHT)
    arr = np.reshape(nums, (z_dim, HEIGHT, WIDTH))

    # Initialize output array.
    arr_output = np.zeros((HEIGHT, WIDTH))

    # Fill output array
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            for k in range(z_dim):
                value = round(arr[k][i][j])
                if value != 2:
                    arr_output[i][j] = value
                    break

    # Replace the 0s with spaces and 1s with @s to make output more readable.
    for row in arr_output:
        print(''.join('@' if int(i) == 1 else ' ' for i in row))

if __name__ == "__main__":
    main()
