def get_points(instructions):
    ''' Find points after each move '''

    latest_point = (0,0)
    path = [latest_point]

    for instruction in instructions.split(','):
        direction = instruction[0]
        distance = int(instruction[1:])

        x = 0
        y = 0

        if direction == 'L':
            x = -distance
        elif direction == 'R':
            x = distance
        elif direction == 'U':
            y = distance
        elif direction == 'D':
            y = -distance
        else:
            raise Exception(f'Invalid direction: {direction}')

        latest_point = (latest_point[0] + x, latest_point[1] + y)
        path.append(latest_point)

    return path

def get_segments(path):
    ''' For x segments return ((x_min, x_max), y) '''
    ''' For y segments return (x, (y_min, y_max)) '''
    x_segs = []
    y_segs = []

    for point_1, point_2 in zip(path[:len(path) - 1], path[1:]):
        x = point_2[0] - point_1[0]
        y = point_2[1] - point_1[1]

        if y == 0:
            x_segs.append(((min(point_2[0], point_1[0]), max(point_2[0], point_1[0])), point_2[1]))
        elif x == 0:
            y_segs.append((point_2[0], (min(point_2[1], point_1[1]), max(point_2[1], point_1[1]))))
        else:
            raise Exception("Have a diagonal line")

    return x_segs, y_segs

def get_intersections(x_segs, y_segs):
    ''' Get the intersection points between x and y segments '''
    crossings = []
    for ((x_min_1, x_max_1), y_1) in x_segs:
        for (x_2, (y_min_2, y_max_2)) in y_segs:
            if x_min_1 <= x_2 <= x_max_1 and y_min_2 <= y_1 <= y_max_2:
                crossings.append((x_2, y_1))
    return crossings

def main():
    with open('./input_01.txt') as input_file:
        lines = input_file.readlines()
        if len(lines) != 2:
            raise Exception('Expected two lines in file, received'.format(len(lines)))

        points_1 = get_points(lines[0].strip())
        points_2 = get_points(lines[1].strip())

        x_segs_1, y_segs_1 = get_segments(points_1)
        x_segs_2, y_segs_2 = get_segments(points_2)

        crossings = []
        crossings.extend(get_intersections(x_segs_1, y_segs_2))
        crossings.extend(get_intersections(x_segs_2, y_segs_1))

        if (0, 0) in crossings:
            crossings.remove((0,0))

        min_point =  min(crossings, key=lambda x: abs(x[0]) + abs(x[1]))
        print("min_point = ", min_point)
        print("distance = ", abs(min_point[0]) + abs(min_point[1]))


if __name__ == '__main__':
    main()
