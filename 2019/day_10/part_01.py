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


if __name__ == '__main__':
    main()