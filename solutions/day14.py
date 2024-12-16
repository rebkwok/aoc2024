import re
from collections import Counter
from utils import read_file_as_lines


robot_re = re.compile(r"p=(?P<col>\d+),(?P<row>\d+) v=(?P<horiz>-?\d+),(?P<vert>-?\d+)")


def empty_grid(rows, cols):
    return [
         [[] for i in range(cols)] for i in range(rows)
    ]


def put_in_quadrants(occupied, rows, cols):
    quadrants = {
        1: [],
        2: [],
        3: [],
        4: [],
    }

    def get_quadrant(point):
        r, c = point
        if 0 <= r < rows // 2:
            if 0 <= c < cols // 2:
                return 1
            if cols // 2 < c < cols:
                return 2
        if rows // 2 < r < rows:
            if 0 <= c < cols // 2:
                return 3
            if cols // 2 < c < cols:
                return 4

    for point in occupied:
        quadrant = get_quadrant(point)
        if quadrant is not None:
            quadrants[quadrant].append(point)
    return quadrants


def draw_tree(grid):
    for row in grid:
        r = ''.join(["#" if it else " " for it in row])
        print(r)


def get_safety_factor(occupied, grid, rows, cols):
    occupied = sorted(occupied)
    quadrants = put_in_quadrants(occupied, rows, cols)

    quadrant_totals = 1
    for quadrant_points in quadrants.values():
        quadrant_total = 0
        for point in quadrant_points:
            robots = grid[point[0]][point[1]]
            if robots:
                quadrant_total += len(robots)
        quadrant_totals *= quadrant_total
    return quadrant_totals   


def part1(input_path):
    rows = 103
    cols = 101

    grid = empty_grid(rows, cols)
    data = read_file_as_lines(input_path)
    
    occupied = set()
    for robot in data:
        groups = robot_re.match(robot).group
        velocity = (int(groups("horiz")), int(groups("vert")))
        row, col = int(groups("row")), int(groups("col"))
        occupied.add((row, col))
        value = grid[row][col]
        value.append(velocity)
        grid[row][col] = value
        
    for  i in range(100):
        new_grid = empty_grid(rows, cols)
        new_occupied = set()
        for pos_r, pos_c in occupied:
            robots = grid[pos_r][pos_c]
            for velocity in robots:
                horiz_vel, vert_vel = velocity
                new_r = (pos_r + vert_vel) % rows
                new_c = (pos_c + horiz_vel) % cols
                new_grid[new_r][new_c].append(velocity)
                new_occupied.add((new_r, new_c))
        grid = new_grid
        occupied = new_occupied

    print(get_safety_factor(occupied, grid, rows, cols))
 

def part2(input_path):

    rows = 103
    cols = 101

    grid = empty_grid(rows, cols)
    data = read_file_as_lines(input_path)

    occupied = set()
    for robot in data:
        groups = robot_re.match(robot).group
        velocity = (int(groups("horiz")), int(groups("vert")))
        row, col = int(groups("row")), int(groups("col"))
        occupied.add((row, col))
        value = grid[row][col]
        value.append(velocity)
        grid[row][col] = value
        
    for  i in range(1, 7384):
        new_grid = empty_grid(rows, cols)
        new_occupied = set()
        for pos_r, pos_c in occupied:
            robots = grid[pos_r][pos_c]
            for velocity in robots:
                horiz_vel, vert_vel = velocity
                new_r = (pos_r + vert_vel) % rows
                new_c = (pos_c + horiz_vel) % cols
                new_grid[new_r][new_c].append(velocity)
                new_occupied.add((new_r, new_c))
        grid = new_grid
        occupied = new_occupied

        row_counter = Counter([r for (r, c) in occupied])
        most_common = row_counter.most_common(2)
        if most_common[0][1] >= 31 and most_common[1][1] >= 31:
        # if row_counter[79] >= 31 and row_counter[47] >= 31:
            print(i)
            draw_tree(grid)


# Attempts to see patterns in part 2
# Eventually found by seeing the trend to a horizontal top/bottom line and
# looking for a high rate of robots on the most common 2 rows
def mirror_rate(quadrants, mid_y):
    """
    quadrants
    1  2
    3  4

    . x   . .
    . .   . .
    
    . x   x .
    . .   . .

    {
        1: [(0, 1)],
        2: [],
        3: [(3, 1)],
        4: [(3, 3)]
    }

    for point in quadrant 1, is corresponding reflected point in quadrant 2?
      - reflection of (0, 1) is (0, 3)
      - x2 == x1, y2 = midy + (midy - y1)
      - 0, 2 + (2 - 1)
      - 0, 3
    
    for point in quadrant 3, is corresponding reflected point in quadrant 4?    
      - reflection of (3, 1) is (3, 3)
      - x4 == x3, y4 = midy + (midy - y3)
      - 3, 2 + (2 - 1)
      - 3, 3
    """
    
    def get_mirror(point):
        r, c = point
        return (r, mid_y + mid_y - c)
    
    total_lhs_points = sum((len(v) for v in [quadrants[1] + quadrants[3]]))
    mirrored = 0
    for point in quadrants[1]:
        mirror = get_mirror(point)
        if mirror in set(quadrants[2]):
            mirrored += 1
    
    for point in quadrants[3]:
        mirror = get_mirror(point)
        if mirror in set(quadrants[4]):
            mirrored += 1
    return mirrored/total_lhs_points


def dispersed_rate(grid, rows, cols):
    mid_x = rows // 2
    mid_y = cols // 2
    max_distance = mid_x * mid_y

    all_points = sum([[(i, j)] * len(grid[i][j]) for i in range(rows) for j in range(cols)], [])
    total = len(all_points) * max_distance
    distance = 0
    for point in all_points:
        distance += (abs(point[0] - mid_x) * abs(point[1] - mid_y))
    
    return distance / total


def proximity_count(grid, rows, cols):
    all_points = sum([[(i, j)] * len(grid[i][j]) for i in range(rows) for j in range(cols)], [])
    point_counter = Counter(all_points)
    points_touching = 0

    for (r, c) in all_points:
        if point_counter[(r, c)] > 1:
            points_touching += 1
        else:
            near_points = [
                (r, c + 1), (r, c - 1), (r + 1, c), (r -1, c)
            ]
            if any(point in all_points for point in near_points):
                points_touching += 1

    return points_touching / len(all_points)


def robots_per_point(occupied, grid):
    all_robots = sum(len(grid[i][j]) for (i, j) in occupied)
    occupied_points = len(occupied)
    return all_robots / occupied_points
 