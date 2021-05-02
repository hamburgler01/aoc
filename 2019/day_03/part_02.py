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
    '''
    For x segments return ((x_min, x_max), y)
    For y segments return (x, (y_min, y_max))
    '''

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

def get_delays(crossings, points):
    '''
    Get the signal delay for each crossing.
    Return a map from the crossing to the corresponding delay.
    '''

    delays = {}

    for crossing in crossings:
        distance = 0

        for point_1, point_2 in zip(points[:len(points) - 1], points[1:]):
            x = point_2[0] - point_1[0]
            y = point_2[1] - point_1[1]

            # Calculate distance if the point lies on the current vertical segment.
            if y == 0:
                min_x = min(point_1[0], point_2[0])
                max_x = max(point_1[0], point_2[0])
                if point_2[1] == crossing[1] and min_x <= crossing[0] <= max_x:
                    distance += abs(crossing[0] - point_1[0])
                    delays[crossing] = distance
                    break

            # Calculate distance if the point lies on the current horizontal segment.
            if x == 0:
                min_y = min(point_1[1], point_2[1])
                max_y = max(point_1[1], point_2[1])
                if point_2[0] == crossing[0] and min_y <= crossing[1] <= max_y:
                    distance += abs(crossing[1] - point_1[1])
                    delays[crossing] = distance
                    break

            # Calculate distance if the point does not lie on the current segment.
            distance += abs(x) + abs(y)

    return delays

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

        delays_1 = get_delays(crossings, points_1)
        delays_2 = get_delays(crossings, points_2)

        min_delay = min(delays_1[crossing] + delays_2[crossing] for crossing in crossings)
        print("Minimum delay = ", min_delay)


if __name__ == '__main__':
    main()
