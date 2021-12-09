from collections import defaultdict
from random import choice

class Computer:
    def __init__(self, intcodes):
        self.intcodes = intcodes[:]
        self.index = 0
        self.relative_base = 0
        self.output = 0
        self.locations = defaultdict(lambda: 'x')
        self.location = (0, 0)
        self.movement = -1
        self.oxygen_found = False


    def _get_input(self):
        while True:
            movement = choice([1, 2, 3, 4])
            if movement == 1: potential_location = self.locations[(self.location[0], self.location[1] + 1)]
            if movement == 2: potential_location = self.locations[(self.location[0], self.location[1] - 1)]
            if movement == 3: potential_location = self.locations[(self.location[0] - 1, self.location[1])]
            if movement == 4: potential_location = self.locations[(self.location[0] + 1, self.location[1])]
            if potential_location != '#':
                self.movement = movement
                break
        return self.movement


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

    def print_grid(self):
        self.locations[(0, 0)] = 'O'
        for i in range(-50, 50):
            for j in range(-50, 50):
                print(self.locations[(i, j)], end='')
            print('')

    def compute(self):
        """ Loop over intcodes and process the """
        while self.index < len(self.intcodes) and not self.oxygen_found:
            op_code, pos_codes = self._get_op_and_pos(self.intcodes[self.index])

            if op_code == 1:
                self.intcodes[self._get_i_or_m(self.index, 3, pos_codes)] = self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] + self.intcodes[self._get_i_or_m(self.index, 2, pos_codes)]
                self.index += 4
            elif op_code == 2:
                self.intcodes[self._get_i_or_m(self.index, 3, pos_codes)] = self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] * self.intcodes[self._get_i_or_m(self.index, 2, pos_codes)]
                self.index += 4
            elif op_code == 3:
                self.movement = self._get_input()
                self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)] = self.movement
                self.index += 2
            elif op_code == 4:
                self.output = self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)]
                if self.output == 0:
                    # Drone hit wall.  Position not changed.
                    if self.movement == 1:   self.locations[(self.location[0], self.location[1] + 1)] = '#'
                    elif self.movement == 2: self.locations[(self.location[0], self.location[1] - 1)] = '#'
                    elif self.movement == 3: self.locations[(self.location[0] - 1, self.location[1])] = '#'
                    elif self.movement == 4: self.locations[(self.location[0] + 1, self.location[1])] = '#'
                    else: raise Exception('Illegal movement: {} (output={}'.format(self.movement, self.output))
                elif self.output == 1:
                    # Drone moved one step in the requested direction
                    if self.movement == 1:
                        self.location = (self.location[0], self.location[1] + 1)
                        self.locations[self.location] = '.'
                    elif self.movement == 2:
                        self.location = (self.location[0], self.location[1] - 1)
                        self.locations[self.location] = '.'
                    elif self.movement == 3:
                        self.location = (self.location[0] - 1, self.location[1])
                        self.locations[self.location] = '.'
                    elif self.movement == 4:
                        self.location = (self.location[0] + 1, self.location[1])
                        self.locations[self.location] = '.'
                    else:
                        raise Exception('Illegal movement: {} (output={}'.format(self.movement, self.output))
                elif self.output == 2:
                    if self.movement == 1:
                        self.location = (self.location[0], self.location[1] + 1)
                        self.locations[self.location] = '@'
                    elif self.movement == 2:
                        self.location = (self.location[0], self.location[1] - 1)
                        self.locations[self.location] = '@'
                    elif self.movement == 3:
                        self.location = (self.location[0] - 1, self.location[1])
                        self.locations[self.location] = '@'
                    elif self.movement == 4:
                        self.location = (self.location[0] + 1, self.location[1])
                        self.locations[self.location] = '@'
                    else:
                        raise Exception('Illegal movement: {} (output={}'.format(self.movement, self.output))
                    print('Oxygen located at {}'.format(self.location))
                    self.oxygen_found = True
                else:
                    raise Exception('Illegal output: {}'.format(self.output))
                self.movement = -1

                #print('Output:', self.output)
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

# Run program.
computer_0 = Computer(intcodes)
computer_0.compute()
computer_0.print_grid()
