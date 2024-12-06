from collections import Counter
from utils import read_file_as_grid


def get_matching_indices(grid, current_point, previous_point, target, diagonal_only=False):

    matching_points = []
    row_ix, col_ix = current_point

    if previous_point is None:  
        # starting; matching points can be in any direction as long as they're not off the grid  
        for row in range(row_ix - 1, row_ix + 2):
            if row < 0 or row >= len(grid):
                continue
            for col in range(col_ix - 1, col_ix + 2):
                if col < 0 or col >= len(grid[0]):
                    continue
                if col == col_ix and row == row_ix:
                    continue
                if grid[row][col] == target:
                    matching_points.append((row, col))

    else:
        # We have a previous point, we can only go in one direction
        prev_row, prev_col = previous_point

        if diagonal_only:
            if prev_row == row_ix or prev_col == col_ix:
                return matching_points

        row_diff = row_ix - prev_row
        col_diff = col_ix - prev_col

        target_row = row_ix + row_diff
        target_col = col_ix + col_diff
        
        if (0 <= target_row < len(grid)) and (0 <= target_col < len(grid)):
            if grid[target_row][target_col] == target:
                matching_points.append((target_row, target_col))        

    return matching_points


def find_xmas(grid, row_ix, col_ix):
    if grid[row_ix][col_ix] != "X":
        return 0
    # look for adjacent Ms
    m_points = get_matching_indices(grid, (row_ix, col_ix), None, target="M")
    final_points = []
    for m_point in m_points:
        a_points = get_matching_indices(grid, m_point, (row_ix, col_ix), target="A")
        for a_point in a_points:
            s_points = get_matching_indices(grid, a_point, m_point, target="S")
            final_points.extend(s_points)  
    return len(final_points)


def find_diagonal_mas(grid, row_ix, col_ix):
    if grid[row_ix][col_ix] != "M":
        return []
    
    matching_coords = []
    # look for adjacent As
    a_points = get_matching_indices(grid, (row_ix, col_ix), None, target="A", diagonal_only=True)
    for a_point in a_points:
        s_points = get_matching_indices(grid, a_point, (row_ix, col_ix), target="S", diagonal_only=True)
        for s_point in s_points:
            matching_coords.append(((row_ix, col_ix), a_point, s_point))
    return matching_coords


def part1(input_path):
    grid = read_file_as_grid(input_path)

    rows = len(grid)
    cols = len(grid[0])
    count = 0
    for row_ix in range(0, rows):
        for col_ix in range(0, cols):
            count += find_xmas(grid, row_ix, col_ix)
    print(count)

def part2(input_path):
    grid = read_file_as_grid(input_path)

    rows = len(grid)
    cols = len(grid[0])
    
    mas = []
    for row_ix in range(0, rows):
        for col_ix in range(0, cols):
            coords = find_diagonal_mas(grid, row_ix, col_ix)
            mas.extend(coords)
    
    a_dict = {}
    for coords in mas:
        a_dict.setdefault(coords[1], []).append(coords)

    count = sum(1 for k, v in a_dict.items() if len(v) == 2)
    assert not any(k for k, v in a_dict.items() if len(v) > 2)
    print(count)
