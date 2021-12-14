def field_to_left():
    return field[y][x - 1]


def field_to_right():
    return field[y][x + 1]


def field_above():
    return field[y - 1][x]


def field_below():
    return field[y + 1][x]


def not_leftmost_column():
    return x > 0


def not_rightmost_column():
    return x < max_x - 1


def not_top_row():
    return y > 0


def not_bottom_row():
    return y < max_y - 1


def risk_level_assessment():
    global field, max_x, x, max_y, y
    field = dict(enumerate(line.strip() for line in iter(puzzle_input.readline, '')))
    risk_level = 0
    low_points = set()
    for x in range(max_x := len(field[0])):
        for y in range(max_y := len(field.keys())):
            height = field[y][x]
            if not_leftmost_column() and field_to_left() <= height:
                continue
            if not_rightmost_column() and height >= field_to_right():
                continue
            if not_top_row() and field_above() <= height:
                continue
            if not_bottom_row() and height >= field_below():
                continue
            risk_level += int(height) + 1
            low_points.add((x, y))
    return risk_level, low_points


def basin_points_for(known_points, point_of_interest):
    x, y = point_of_interest
    if point_of_interest in known_points:
        return set()
    if x < 0 or x >= max_x or y < 0 or y >= max_y:
        return set()
    if field[y][x] != '9':
        known_points.add(point_of_interest)
        known_points |= basin_points_for(known_points, (x + 1, y))
        known_points |= basin_points_for(known_points, (x - 1, y))
        known_points |= basin_points_for(known_points, (x, y + 1))
        known_points |= basin_points_for(known_points, (x, y - 1))
    return known_points


def basins(low_points):
    basins = {}
    for low_point in low_points:
        points = set()
        basins |= {low_point: basin_points_for(set(), low_point)}
    return basins


def assess_smoke_basins():
    global risk_level, low_points, largest_basins
    risk_level, low_points = risk_level_assessment()
    all_basins = basins(low_points)
    top_basins = sorted(all_basins.values(), key=lambda v: len(v), reverse=True)
    largest_basins = len(top_basins[0]) * len(top_basins[1]) * len(top_basins[2])


if __name__ == '__main__':
    print("Advent of Code – Day 9: Smoke Basin")
    with open('example.txt') as puzzle_input:
        assess_smoke_basins()
        print(f"Risk assessment resulted in a risk level of {risk_level}")
        print(f"The three largest basins have a combined size of {largest_basins}")
    with open('puzzle_input.txt') as puzzle_input:
        assess_smoke_basins()
        print(f"Risk assessment resulted in a risk level of {risk_level}")
        print(f"The three largest basins have a combined size of {largest_basins}")
