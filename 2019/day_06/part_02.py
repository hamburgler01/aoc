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

# Find the common ancestor fo YOU and SAN.
path_san = d_name_to_node['SAN'].path
for node in d_name_to_node['YOU'].iter_path_reverse():
    if node in path_san:
        common_ancestor = node
        break

# Calculate path distance.
distance = d_name_to_node['SAN'].depth + d_name_to_node['YOU'].depth - 2 * common_ancestor.depth
print("Distance = ", distance - 2)
