def get_input():
    return 5

def get_op_and_pos(intcode):
    ''' Get op and position codes '''
    op_code = intcode % 100
    pos_codes = list(reversed([int(s) for s in list(str(intcode // 100))]))
    return op_code, pos_codes

def get_i_or_m(intcodes, index, offset, pos_codes):
    ''' Depending on the pos_code, return an immediate or memory reference '''
    if offset < 1:
        raise Exception("Illegal offset: ".format(offset))
    pos_code = 0 if offset > len(pos_codes) else pos_codes[offset - 1]
    return intcodes[index + offset] if pos_code == 0 else index + offset

# Store intcodes as a list of integers.
with open('./input_01.txt') as input_file:
    intcodes = [int(num) for num in input_file.read().strip().split(',')]

# Loop over intcodes and process them.
index = 0
while index < len(intcodes):
    op_code, pos_codes = get_op_and_pos(intcodes[index])

    if op_code == 1:
        intcodes[get_i_or_m(intcodes, index, 3, pos_codes)] = intcodes[get_i_or_m(intcodes, index, 1, pos_codes)] + intcodes[get_i_or_m(intcodes, index, 2, pos_codes)]
        index += 4
    elif op_code == 2:
        intcodes[get_i_or_m(intcodes, index, 3, pos_codes)] = intcodes[get_i_or_m(intcodes, index, 1, pos_codes)] * intcodes[get_i_or_m(intcodes, index, 2, pos_codes)]
        index += 4
    elif op_code == 3:
        intcodes[get_i_or_m(intcodes, index, 1, pos_codes)] = get_input()
        index += 2
    elif op_code == 4:
        print("Output = ", intcodes[intcodes[index + 1]])
        index += 2
    elif op_code == 5:
        if intcodes[get_i_or_m(intcodes, index, 1, pos_codes)] != 0:
            index = intcodes[get_i_or_m(intcodes, index, 2, pos_codes)]
        else:
            index += 3
    elif op_code == 6:
        if intcodes[get_i_or_m(intcodes, index, 1, pos_codes)] == 0:
            index = intcodes[get_i_or_m(intcodes, index, 2, pos_codes)]
        else:
            index += 3
    elif op_code == 7:
        intcodes[get_i_or_m(intcodes, index, 3, pos_codes)] = int(intcodes[get_i_or_m(intcodes, index, 1, pos_codes)] < intcodes[get_i_or_m(intcodes, index, 2, pos_codes)])
        index += 4
    elif op_code == 8:
        intcodes[get_i_or_m(intcodes, index, 3, pos_codes)] = int(intcodes[get_i_or_m(intcodes, index, 1, pos_codes)] == intcodes[get_i_or_m(intcodes, index, 2, pos_codes)])
        index += 4
    elif op_code == 99:
        break;
    else:
        raise Exception(f'Illegal instruction opcode: {op_code}')
