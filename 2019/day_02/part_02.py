import copy

# Store intcodes as a list of integers.
with open('./input_01.txt') as input_file:
    intcodes = [int(num) for num in input_file.read().strip().split(',')]


# Get the output associated with associated with particular inputs.
def get_output(intcode_1, intcode_2, intcodes_initial):

    # Set the initial state
    intcodes = copy.copy(intcodes_initial)
    intcodes[1] = intcode_1
    intcodes[2] = intcode_2

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
    return intcodes[0]


expected_output = 19690720

# Loop over intputs until the expected output is achieved.
for input_1 in range(0, 100):
    for input_2 in range(0, 100):
        output = get_output(input_1, input_2, intcodes)
        if output == expected_output:
            print(f'Inputs {input_1} and {input_2} give output {output}')
            exit(0)
print(f'Inputs not found for output {output}')
