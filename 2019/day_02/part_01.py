# Store intcodes as a list of integers.
with open('./input_01.txt') as input_file:
    intcodes = [int(num) for num in input_file.read().strip().split(',')]

# Restore 1202 Program alarm state.
intcodes[1] = 12
intcodes[2] = 2

# Loop over intcodes and process them.
index = 0
while index < len(intcodes):
    if intcodes[index] == 1:
        intcodes[intcodes[index + 3]] = intcodes[intcodes[index + 1]] + intcodes[intcodes[index + 2]]
        index += 4
    elif intcodes[index] == 2:
        intcodes[intcodes[index + 3]] = intcodes[intcodes[index + 1]] * intcodes[intcodes[index + 2]]
        index += 4
    elif intcodes[index] == 99:
        break;
    else:
        raise Exception(f'Illegal instruction: {intcodes[index]}')

print("intcodes[0] = ", intcodes[0])
