from itertools import permutations

class Computer():
    def __init__(self, intcodesX, phase):
        self.intcodes = intcodesX[:]
        self.phase = phase
        self.input_signal = 0
        self.input_call = 0
        self.index = 0

    def _get_input(self):
        if self.input_call == 0:
            self.input_call += 1
            return self.phase
        else:
            return self.input_signal

    def _get_op_and_pos(self, intcode):
        ''' Get op and position codes '''
        op_code = intcode % 100
        pos_codes = list(reversed([int(s) for s in list(str(intcode // 100))]))
        return op_code, pos_codes

    def _get_i_or_m(self, index, offset, pos_codes):
        ''' Depending on the pos_code, return an immediate or memory reference '''
        if offset < 1:
            raise Exception("Illegal offset: ".format(offset))
        pos_code = 0 if offset > len(pos_codes) else pos_codes[offset - 1]
        return self.intcodes[index + offset] if pos_code == 0 else index + offset

    def compute(self, input_signal):
        ''' Loop over intcodes and process the '''
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
                self.index += 2
                return self.intcodes[self.intcodes[self.index + 1 - 2]]  # Account for adding 2 to index in line above.
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
            elif op_code == 99:
                self.index += 1
                return None
            else:
                raise Exception(f'Illegal instruction opcode: {op_code}')
        return None

# Store intcodes as a list of integers.
with open('./input_01.txt') as input_file:
    intcodes = [int(num) for num in input_file.read().strip().split(',')]


# Loop over permutations and find the max signal.
perms = permutations(range(5, 10))
max_signal = -1
for perm in perms:
    computer_0 = Computer(intcodes, perm[0])
    computer_1 = Computer(intcodes, perm[1])
    computer_2 = Computer(intcodes, perm[2])
    computer_3 = Computer(intcodes, perm[3])
    computer_4 = Computer(intcodes, perm[4])

    last_compute = 0
    while True:
        last_compute = computer_0.compute(last_compute)
        if last_compute is None:
            break

        last_compute = computer_1.compute(last_compute)
        if last_compute is None:
            break

        last_compute = computer_2.compute(last_compute)
        if last_compute is None:
            break

        last_compute = computer_3.compute(last_compute)
        if last_compute is None:
            break

        last_compute = computer_4.compute(last_compute)
        if last_compute is None:
            break
        else:
            last_compute_4 = last_compute

    max_signal = max(max_signal, last_compute_4)

print("Max Signal = ", max_signal)
