from collections import defaultdict

class Robot:
    def __init__(self):
        self.location = (0,0)
        self.direction = 'up'
        self.hull = defaultdict(int)
        self.painted_once = set()

        # Set original location to white.
        self.paint(1)

    def move(self, turn):
        # Rotate robot.
        if turn == 0: # Turn left 90deg
            if self.direction == 'up': self.direction = 'left'
            elif self.direction == 'left': self.direction = 'down'
            elif self.direction == 'down': self.direction = 'right'
            elif self.direction == 'right': self.direction = 'up'
            else:
                print(f'Illegal direction when turning left: {self.direction}')
                exit(1)
        else: # Turn right 90deg
            if self.direction == 'up': self.direction = 'right'
            elif self.direction == 'right': self.direction = 'down'
            elif self.direction == 'down': self.direction = 'left'
            elif self.direction == 'left': self.direction = 'up'
            else:
                print(f'Illegal direction when turning right: {self.direction}')
                exit(1)

        # Move in x-y plane.
        x, y = self.location
        if self.direction == 'up': self.location = x, y + 1
        elif self.direction == 'left': self.location = x - 1, y
        elif self.direction == 'down': self.location = x, y - 1
        elif self.direction == 'right': self.location = x + 1, y
        else:
            print(f'Illegal direction when setting direction: {self.direction}')
            exit(1)

    def paint(self, color):
        self.hull[self.location] = color
        self.painted_once.add(self.location)

    def get_color(self):
        return self.hull[self.location]

    def get_painted_once(self):
        return len(self.painted_once)

    def display(self):
        min_x = min(x for x, _ in self.painted_once)
        max_x = max(x for x, _ in self.painted_once)
        min_y = min(y for _, y in self.painted_once)
        max_y = max(y for _, y in self.painted_once)

        for j in reversed(range(min_y, max_y + 1)):
            for i in range(min_x, max_x + 1):
                if self.hull[(i, j)] == 1:
                    print('#', end='')
                else:
                    print(' ', end='')
            print('')

class Computer:
    def __init__(self, intcodes):
        self.intcodes = intcodes[:]
        self.index = 0
        self.relative_base = 0
        self.robot = Robot()
        self.is_first_output = True

    def _get_input(self):
        return self.robot.get_color()

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

    def get_painted_once(self):
        return self.robot.get_painted_once()

    def display(self):
        self.robot.display()

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
                output = self.intcodes[self._get_i_or_m(self.index, 1, pos_codes)]
                if self.is_first_output:
                    self.robot.paint(output)
                else:
                    self.robot.move(output)
                self.is_first_output ^= 1
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
print("Painted once:", computer_0.get_painted_once())
computer_0.display()
