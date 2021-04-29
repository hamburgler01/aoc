import math

def get_fuel(mass):
    ''' Calculate fuel as a function of mass '''
    if mass < 0:
        raise Exception(f'negative mass of {mass}');
    return math.floor(mass / 3) - 2;

with open("./input_01.txt") as input_file:
    total_fuel = sum(get_fuel(int(line.strip())) for line in input_file)

print(f'Total fuel = {total_fuel}')
        
