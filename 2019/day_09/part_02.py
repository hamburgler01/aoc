from itertools import permutations


class Computer:
    def __init__(self, intcodes, phase):
        self.intcodes = intcodes[:]
        self.phase = phase
        self.input_signal = 0
        self.input_call = 0
        self.index = 0
        self.relative_base = 0

    def _get_input(self):
        if self.input_call == 0:
            self.input_call += 1
            return self.phase
        else:
            return self.input_signal

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

    def compute(self, input_signal):
        """ Loop over intcodes and process the """
        self.input_signal = input_signal
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
                print(">", self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)])
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


# Store intcodes as a list of integers.
with open('./input_01.txt') as input_file:
    intcodes = [int(num) for num in input_file.read().strip().split(',')]
    intcodes.extend([0] * 10000000)

computer_0 = Computer(intcodes, 2)
computer_0.compute(2)