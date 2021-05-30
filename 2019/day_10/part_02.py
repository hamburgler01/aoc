import math
import collections
import functools


def get_coordinates():
    with open('input_01.txt') as input:
        coordinates = []
        x = 0
        y = 0
        for line in input:
            x = 0
            for char in line:
                if char == '#':
                    coordinates.append((x, y))
                x += 1
            y += 1
    return coordinates


def get_m_and_b(point_1, point_2):
    if point_2[0] == point_1[0]:
        return None, None
    slope = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
    intercept = point_2[1] - slope * point_2[0]
    return slope, intercept


def get_side_of_origin(origin, point):
    if origin[0] == point[0]:
        return point[1] > origin[1]
    if origin[1] == point[1]:
        return point[0] > origin[0]
    return point[1] > origin[1]


def get_angle_dictionary(origin, coordinates):
    """
    Return a dictionary where the key is the angle relative to the origin
    and the value is a list of all coordinates with that angle, sorted by
    distance from the origin.
    """
    def rotate(o, p):
        theta = math.radians(-270)
        ox, oy = o
        px, py = p

        qx = ox + math.cos(theta) * (px - ox) - math.sin(theta) * (py - oy)
        qy = oy + math.sin(theta) * (px - ox) + math.cos(theta) * (py - oy)

        return qx, qy

    def calc_distance(p):
        return math.sqrt(math.pow(origin[0] - p[0], 2) + math.pow(origin[1] - p[1], 2))

    def cmp_distance(p1, p2):
        if calc_distance(p1) < calc_distance(p2):
            return -1
        elif calc_distance(p1) > calc_distance(p2):
            return 1
        else:
            return  0

    d = collections.defaultdict(list)
    for point in coordinates:
        if point == origin:
            continue
        rotated_point = rotate(origin, point)
        angle = math.atan2(rotated_point[1] - origin[1], rotated_point[0] - origin[0])
        if angle < 0:
            angle += 2 * math.pi
        d[round(angle, 5)].append(point)
    for key in d.keys():
        d[key].sort(key=functools.cmp_to_key(cmp_distance))
        #print("++>     d[key]=", d[key])
    #print(d)
    return d


def main():
    max_visible = ((0, 0), 0)

    # Loop over each asteroid that you view from.
    coordinates = get_coordinates()
    for coordinate in coordinates:
        lines_and_sides = []
        # Loop over all asteroids except the one from which you are viewing.
        for coordinate_other in coordinates:
            if coordinate != coordinate_other:
                # Store the line on which the asteroid falls as well as the side of the base on which it's on.
                slope, intercept = get_m_and_b(coordinate, coordinate_other)
                lines_and_sides.append((None if slope is None else round(slope, 5),
                                        None if intercept is None else round(intercept, 5),
                                        get_side_of_origin(coordinate, coordinate_other)))

        # Exclude asteroids that fall on the same line and lie on the same side of the station as another asteroid.
        visible = set(lines_and_sides)

        if len(visible) > max_visible[1]:
            max_visible = (coordinate, len(visible))

    print(f'Location: {max_visible[0]}    Visible: {max_visible[1]}')
    station = max_visible[0]
    angle_dict = get_angle_dictionary(station, coordinates)

    count = 1
    asteroid_200 = (0, 0)
    while True:
        asteroids_remaining = False
        for angle in sorted(angle_dict.keys()):
            #print("----> ", angle)
            #print(angle_dict[angle])
            if len(angle_dict[angle]) != 0:
                #print(count, angle_dict[angle][0])
                if count == 200:
                    asteroid_200 = angle_dict[angle][0]
                angle_dict[angle].pop(0)
                count += 1
                asteroids_remaining = True
        if not asteroids_remaining:
            break

    x_200, y_200 = asteroid_200
    print("Asteroid 200:", asteroid_200, "  Solution:", x_200 * 100 + y_200)


if __name__ == '__main__':
    main()