from anytree import Node, RenderTree
from collections import defaultdict

# Map name of parent to names of its children.
d_parent_to_children = defaultdict(list)

# Map name to the associated node.
com = Node('COM')
d_name_to_node = {'COM': com}

with open('./input_01.txt') as input_file:
    for line in input_file.readlines():
        parent, child = line.strip().split(')')
        d_name_to_node[child] = Node(child)
        d_parent_to_children[parent].append(child)

# Associate each node with its children.
for parent, children in d_parent_to_children.items():
    d_name_to_node[parent].children = [d_name_to_node[child] for child in children]

# The depth of a node its number of orbits.
orbits = 0
for node in d_name_to_node.values():
    orbits += node.depth

print("Total orbits: ", orbits)
