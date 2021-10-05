from itertools import combinations
import re
from copy import deepcopy
import  numpy as np
import itertools

positions_x = []
positions_y = []
positions_z = []
velocities_x = []
velocities_y = []
velocities_z = []

initial_velocities = []

def get_variables(dimension):
    if dimension == 0:
        return positions_x, velocities_x
    elif dimension == 1:
        return positions_y, velocities_y
    elif dimension == 2:
        return positions_z, velocities_z
    else:
        raise Exception

def update_velocity(dimension):
    positions, velocities = get_variables(dimension)

    for index_moon_1, index_moon_2 in combinations(range(len(positions)), 2):
        if positions[index_moon_1] < positions[index_moon_2]:
            velocities[index_moon_1] += 1
            velocities[index_moon_2] -= 1
        elif positions[index_moon_2] < positions[index_moon_1]:
            velocities[index_moon_2] += 1
            velocities[index_moon_1] -= 1

def update_position(dimension):
    positions, velocities = get_variables(dimension)

    for index_moon in range(len(positions)):
        positions[index_moon] += velocities[index_moon]

def main():
    with open('input_01.txt') as input_file:
        for line in input_file:
            coordinates = re.search('<x=(.+), y=(.+), z=(.+)>', line.strip())
            positions_x.append(int(coordinates.group(1)))
            positions_y.append(int(coordinates.group(2)))
            positions_z.append(int(coordinates.group(3)))
            velocities_x.append(0)
            velocities_y.append(0)
            velocities_z.append(0)
            initial_velocities.append(0)

    steps = [0, 0, 0]
    for dimension in range(len(steps)):
        _, velocities = get_variables(dimension)

        for step in itertools.count():
            update_velocity(dimension)
            update_position(dimension)
            steps[dimension] += 1

            if velocities == initial_velocities:
                break

    print("Cycles:", np.lcm.reduce(steps) * 2)
    return

if __name__ == '__main__':
    main()
