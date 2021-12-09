from collections import defaultdict

def calculate(fuel_amount):
    # Parse input into dictionary.
    input_file = 'input_01.txtx'

    with open(input_file) as file:
        reactions_input = [line[:-1] for line in file]

    reactions = {}
    for reaction in reactions_input:
        reaction_split = reaction.split(' => ')
        output_amount, output_type = reaction_split[-1].split(' ')
        inputs = {}
        input_split = reaction_split[0].split(', ')
        for input in input_split:
            input_amount, input_type = input.split(' ')
            inputs[input_type] = int(input_amount)
        reactions[output_type] = {'out': int(output_amount), 'in': inputs}

    # Perform reactions
    chem_needs = defaultdict(int)
    chem_needs['FUEL'] = fuel_amount

    chem_have = defaultdict(int)
    ore = 0

    while chem_needs:
        item = list(chem_needs.keys())[0]

        if chem_needs[item] <= chem_have[item]:
            chem_have[item] -= chem_needs[item]
            del chem_needs[item]
            continue

        num_needed = chem_needs[item] - chem_have[item]
        del chem_have[item]
        del chem_needs[item]
        num_produced = reactions[item]['out']

        num_reactions = num_needed // num_produced if num_needed % num_produced == 0 else num_needed // num_produced + 1

        chem_have[item] += num_reactions * num_produced - num_needed

        for chem in reactions[item]['in']:
            if chem == 'ORE':
                ore += reactions[item]['in'][chem] * num_reactions
            else:
                chem_needs[chem] += reactions[item]['in'][chem] * num_reactions

    return ore

low = 1e12 // calculate(1)
high = low * 10

while calculate(high) < 1e12:
    low = high
    high = 10 * low

while low < high - 1:
    mid = (low + high) // 2
    ore = calculate(mid)
    if ore < 1e12:
        low = mid
    elif ore > 1e12:
        high = mid
    else:
        break

print("Fuel:  ", int(mid) - 1)