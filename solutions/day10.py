from utils import read_file_as_grid



def get_next_positions(current_position, current_value, grid):
    next_value = current_value + 1
    row, col = current_position
    adjacent_positions = [
        (row + 1, col),
        (row - 1, col),
        (row, col +1 ),
        (row, col - 1)
    ]
    next_positions = set()
    for rpos, cpos in adjacent_positions:
        if (0 <= rpos < len(grid)) and (0 <= cpos < len(grid[0])):
            if grid[rpos][cpos] == next_value:
                next_positions.add((rpos, cpos))
    
    return next_positions


def trailhead_score_pt_1(trailhead, grid):
    to_visit = [trailhead]
    visited = set()

    score = 0

    while to_visit:
        current_position = to_visit.pop()
        visited.add(current_position)
        current_value = grid[current_position[0]][current_position[1]]
        if current_value == 9:
            score += 1
        else:
            next_positions = get_next_positions(current_position, current_value, grid)
            for position in next_positions:
                if position not in visited:
                    to_visit.append(position)
    return score


def trailhead_score_pt_2(trailhead, grid):
    to_visit = [trailhead]

    score = 0

    while to_visit:
        current_position = to_visit.pop()
        current_value = grid[current_position[0]][current_position[1]]

        if current_value != 9:
            next_positions = get_next_positions(current_position, current_value, grid)
            for position in next_positions:
                to_visit.append(position)
        else:
            score += 1
    return score


def get_grid_and_trailheads(input_path):
    grid = read_file_as_grid(input_path, apply_fn=int)
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                trailheads.append((i, j))
    
    return grid, trailheads


def part1(input_path):
    grid, trailheads = get_grid_and_trailheads(input_path)
    print(sum(trailhead_score_pt_1(trailhead, grid) for trailhead in trailheads))


def part2(input_path):
    grid, trailheads = get_grid_and_trailheads(input_path)
    print(sum(trailhead_score_pt_2(trailhead, grid) for trailhead in trailheads))
