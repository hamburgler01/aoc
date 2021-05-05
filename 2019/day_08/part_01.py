import numpy as np
import sys

WIDTH = 25
HEIGHT = 6

def get_count(row, n):
    ''' Get number of n's in the row '''
    return ''.join([str(i) for i in row]).count(str(n))

def main():
    # Read input as a 1-D array of single numbers
    with open('input_01.txt') as input_file:
        nums = [int(i) for i in list(input_file.readline().strip())]

    # Reshape input into a 2-D array.
    # Each sub-array represents a layer (which contains WIDTH * HEIGHT entries)
    arr = np.reshape(nums, (len(nums) // (WIDTH * HEIGHT), WIDTH * HEIGHT))

    # Determine the row with the least number of 0s.
    min_zeros = sys.maxsize
    for row in arr:
        count_zeros = get_count(row, 0)
        if count_zeros < min_zeros:
            min_zeros = count_zeros
            min_row = row

    # Result is the number of ones times the number of twos in the row with the least number of 0s.
    print('ones * twos = ', get_count(min_row, 1) * get_count(min_row, 2))


if __name__ == "__main__":
    main()
