import math
import collections
import functools


def get_coordinates():
    """ Return a list of coordinates of all asteroids """
    with open('input_01.txt') as input:
        coordinates = []
        x, y = 0, 0
        for line in input:
            x = 0
            for char in line:
                if char == '#':
                    coordinates.append((x, y))
                x += 1
            y += 1
    return coordinates


def get_m_and_b(point_1, point_2):
    """ Determine the slope intercept of the line passing through two points """
    p1_x, p1_y = point_1
    p2_x, p2_y = point_2

    if p2_x == p1_x:
        return None, None
    slope = (p2_y - p1_y) / (p2_x - p1_x)
    intercept = p2_y - slope * p2_x

    return slope, intercept


def get_side_of_origin(origin, point):
    """ Determine which 'side' of the origin a point lies on """
    o_x, o_y = origin
    p_x, p_y = point

    if o_x == p_x:
        return p_y > o_y
    if o_y == p_y:
        return p_x > o_x
    return p_y > o_y


def get_angle_dictionary(origin, coordinates):
    """
    Return a dictionary where the key is the angle relative to the origin
    and the value is a list of all coordinates with that angle, sorted by
    distance from the origin.
    """
    def rotate_90(o, p):
        """ Rotate a point 90 degrees with respect to the origin """
        theta = math.radians(90)
        ox, oy = o
        px, py = p

        qx = ox + math.cos(theta) * (px - ox) - math.sin(theta) * (py - oy)
        qy = oy + math.sin(theta) * (px - ox) + math.cos(theta) * (py - oy)

        return qx, qy

    def calc_distance(p1, p2):
        """ Determine the distance between two points """
        p1_x, p1_y = p1
        p2_x, p2_y = p2
        return math.sqrt(math.pow(p1_x - p2_x, 2) + math.pow(p1_x - p2_x, 2))

    def cmp_distance(p1, p2):
        """ Compare the distance between points and the origin """
        if calc_distance(origin, p1) < calc_distance(origin, p2):
            return -1
        elif calc_distance(origin, p1) > calc_distance(origin, p2):
            return 1
        else:
            return 0

    # Mapping from angle between station and asteroid and all asteroids lying at that angle.
    d = collections.defaultdict(list)

    # Loop over all asteroids.
    for point in coordinates:
        # Exclude the station
        if point == origin:
            continue
        # atan2() measures angles from the horizontal x axis but the gun that destroys the asteroids starts
        # shooting in the vertical direction.  A rotation of 90 deg therefore necessary to use atan2() with the
        # coordinate system defined for this problem.
        rotated_point = rotate_90(origin, point)
        angle = math.atan2(rotated_point[1] - origin[1], rotated_point[0] - origin[0])

        # Ensure that all angles are positive by using the fact that a circle has a periodicity of 2 * PI.
        if angle < 0:
            angle += 2 * math.pi
        d[round(angle, 5)].append(point)

    # Sort all asteroids lying a certain angle by their distance from the station.
    for key in d.keys():
        d[key].sort(key=functools.cmp_to_key(cmp_distance))
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

        # Determine if the current station location corresponds to the maximum number of visible asteroids.
        if len(visible) > max_visible[1]:
            max_visible = (coordinate, len(visible))

    # Determine the location of the station.
    print(f'Location: {max_visible[0]}    Visible: {max_visible[1]}')
    station = max_visible[0]

    # Get a dictionary mapping angles to all asteroids located at that angle.
    angle_dict = get_angle_dictionary(station, coordinates)

    # Moving clockwise from the vertical, remove one asteroid per angle in each loop
    count = 1
    asteroid_200 = (0, 0)
    while True:
        asteroids_remaining = False
        for angle in sorted(angle_dict.keys()):
            if len(angle_dict[angle]) != 0:
                if count == 200:
                    asteroid_200 = angle_dict[angle][0]
                angle_dict[angle].pop(0)
                count += 1
                asteroids_remaining = True
        if not asteroids_remaining:
            break

    # Use the 200th destroyed asteroid to obtain the solution.
    x_200, y_200 = asteroid_200
    print("Asteroid 200:", asteroid_200, "  Solution:", x_200 * 100 + y_200)


if __name__ == '__main__':
    main()