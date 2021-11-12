from collections import defaultdict

class Computer:
    def __init__(self, intcodes):
        self.intcodes = intcodes[:]
        self.intcodes[0] = 2 # Set to free play
        self.index = 0
        self.relative_base = 0
        self.is_first_output = True
        self.output = []
        self.screen = dict()
        self.score = 0
        self.paddle = (0, 0)
        self.ball = (0, 0)

    def _get_input(self):
        if self.ball[0] < self.paddle[0]:
            return -1
        if self.ball[0] > self.paddle[0]:
            return 1
        return 0

    def _get_op_and_pos(self, intcode):
        """ Get op and position codes """
        op_code = intcode % 100
        pos_codes = list(reversed([int(s) for s in list(str(intcode // 100))]))
        return op_code, pos_codes

    def _get_i_or_m(self, index, offset, pos_codes):
        """ Depending on the pos_code, return an immediate, memory, or relative reference """
        if offset < 1:
            raise Exception("Illegal offset: ".format(offset))
        pos_code = 0 if offset > len(pos_codes) else pos_codes[offset - 1]

        if pos_code == 0: # Memory
            return self.intcodes[index + offset]
        elif pos_code == 1: # Immediate
            return index + offset
        elif pos_code == 2: # Relative
            return self.intcodes[index + offset] + self.relative_base
        else:
            raise Exception("Illegal position code: {}".format(pos_code))

    def compute(self):
        """ Loop over intcodes and process the """
        while self.index < len(self.intcodes):
            op_code, pos_codes = self._get_op_and_pos(self.intcodes[self.index])

            if op_code == 1:
                self.intcodes[self._get_i_or_m(self.index, 3, pos_codes)] = self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] + self.intcodes[self._get_i_or_m(self.index, 2, pos_codes)]
                self.index += 4
            elif op_code == 2:
                self.intcodes[self._get_i_or_m(self.index, 3, pos_codes)] = self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] * self.intcodes[self._get_i_or_m(self.index, 2, pos_codes)]
                self.index += 4
            elif op_code == 3:
                self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] = self._get_input()
                self.index += 2
            elif op_code == 4:
                self.output.append(self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)])
                if len(self.output) == 3:
                    x, y, i = self.output[0], self.output[1], self.output[2]
                    if x == -1 and y == 0:
                        self.score = i
                    else:
                        self.screen[(x,y)] = i
                        if i == 3:
                            self.paddle = (x, y)
                        elif i == 4:
                            self.ball = (x, y)
                    self.output = []
                self.index += 2
            elif op_code == 5:
                if self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] != 0:
                    self.index = self.intcodes[self._get_i_or_m(self.index, 2, pos_codes)]
                else:
                    self.index += 3
            elif op_code == 6:
                if self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] == 0:
                    self.index = self.intcodes[self._get_i_or_m(self.index, 2, pos_codes)]
                else:
                    self.index += 3
            elif op_code == 7:
                self.intcodes[self._get_i_or_m(self.index, 3, pos_codes)] = int(self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] < self.intcodes[self._get_i_or_m(self.index, 2, pos_codes)])
                self.index += 4
            elif op_code == 8:
                self.intcodes[self._get_i_or_m(self.index, 3, pos_codes)] = int(self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] == self.intcodes[self._get_i_or_m(self.index, 2, pos_codes)])
                self.index += 4
            elif op_code == 9:
                self.relative_base += self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)]
                self.index += 2
            elif op_code == 99:
                self.index += 1
                return None
            else:
                raise Exception(f'Illegal instruction opcode: {op_code}')
        return None

    def get_output(self):
        return self.output

    def get_score(self):
        return self.score


# Store intcodes as a list of integers.
with open('./input_01.txt') as input_file:
    intcodes = [int(num) for num in input_file.read().strip().split(',')]
    intcodes.extend([0] * 10000000)

# Run program.
computer_0 = Computer(intcodes)
computer_0.compute()

# Determine the number of block tiles and score.
output = computer_0.get_output()

output_x, output_y, output_i = output[0::3], output[1::3], output[2::3]
point_to_instruction = zip(zip(output_x, output_y), output_i)

block_tiles = 0
for (x, y), i in point_to_instruction:
    if i == 2:
        block_tiles += 1

print("Block Tiles:", block_tiles)
print("Score:", computer_0.get_score())