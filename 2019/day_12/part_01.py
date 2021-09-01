from itertools import combinations
import re

positions = []
velocities = []

def update_velocity():
    for index_moon_1, index_moon_2 in combinations(range(len(positions)), 2):
        for dimension, coord_1, coord_2 in zip(range(3), positions[index_moon_1], positions[index_moon_2]):
            if coord_1 < coord_2:
                velocities[index_moon_1][dimension] += 1
                velocities[index_moon_2][dimension] -= 1
            elif coord_2 < coord_1:
                velocities[index_moon_2][dimension] += 1
                velocities[index_moon_1][dimension] -= 1

def update_position():
    for index_moon in range(len(positions)):
        for dimension in range(3):
            positions[index_moon][dimension] += velocities[index_moon][dimension]

def calculate_energy():
    total_energy = 0
    for index in range(len(positions)):
        total_energy += sum(abs(i) for i in positions[index]) * sum(abs(i) for i in velocities[index])
    return total_energy

def main():
    with open('input_01.txt') as input_file:
        for line in input_file:
            coordinates = re.search('<x=(.+), y=(.+), z=(.+)>', line.strip())
            positions.append([int(coordinates.group(1)), int(coordinates.group(2)), int(coordinates.group(3))])
            velocities.append([0, 0, 0])

    for step in range(1000):
        update_velocity()
        update_position()

    print("Energy = ", calculate_energy())

if __name__ == '__main__':
    main()
