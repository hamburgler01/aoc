import math

def get_fuel(mass):
    return calc_fuel(mass) - mass
    
def calc_fuel(mass):    
    return 0 if mass <= 0 else mass + calc_fuel(math.floor(mass / 3) - 2);

with open("./input_01.txt") as input_file:
    total_fuel = sum(get_fuel(int(line.strip())) for line in input_file)

print(f'Total fuel = {total_fuel}')
        
