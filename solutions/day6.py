from collections import Counter
from copy import deepcopy
from utils import read_file_as_grid


class Guard:

    def __init__(self, starting_grid):
        self.rows = starting_grid
        self.cols = list(zip(*self.rows))
        self.location, self.direction = self.get_start()
        self.visited = [self.location]
        self.changed_direction = {}
        self.done = False

    def get_start(self):
        directions = ["^", ">", "<", "v"]

        for row in range(len(self.rows)):
            for col in range(len(self.rows[0])):
                if self.rows[row][col] in directions:
                    return (row, col), self.rows[row][col]

    def move(self):
        row, col  = self.location
        direction = -1 if self.direction in ["^", "<"] else 1
        if self.direction in ["^", "V"]:
            # Moving in a column, up or down
            target_col = self.cols[col]
            current_pos = row
            while True:
                current_pos += direction
                if not (0 <= current_pos < len(self.rows)):
                    # we've moved off the grid, done
                    self.done = True
                    return
                if target_col[current_pos] == "#":
                    # We're at an obstacle, turn right and finish move
                    self.turn_right()
                    return
                self.visited.append((current_pos, col))
                self.location = (current_pos, col)
        else:
            # Moving in a row, L or R
            target_row = self.rows[row]
            current_pos = col
            while True:
                current_pos += direction
                if not (0 <= current_pos < len(self.cols)):
                    # we've moved off the grid, done
                    self.done = True
                    return
                if target_row[current_pos] == "#":
                    # We're at an obstacle, turn right and finish move
                    self.turn_right()
                    return
                self.visited.append((row, current_pos))
                self.location = (row, current_pos)

    def is_loop(self):
        counter = Counter(self.changed_direction)
        most_common_4 = dict(counter.most_common(4))
        return most_common_4 and max(most_common_4.values()) >= 3

    def go(self):
        while True:
            if self.is_loop():
                # in a loop, stop
                break   
            self.move()
            if self.done:
                break
    
    def turn_right(self):
        next_direction = {
            "^": ">",
            ">": "V",
            "V": "<",
            "<": "^"
        }
        self.direction = next_direction[self.direction]
        self.changed_direction.setdefault(self.location, 0)
        self.changed_direction[self.location] += 1


def part1(input_path):
    grid = read_file_as_grid(input_path)
    guard = Guard(grid)
    guard.go()
    print(len(set(guard.visited)))


def part2(input_path):
    grid = read_file_as_grid(input_path)
    guard = Guard(grid)

    possible_obstacles = []
    for row in range(len(grid)):
        for col in range(len(grid)):
            if (row, col) != guard.location and grid[row][col] != "#":
                possible_obstacles.append((row, col))
    print(len(possible_obstacles))
    looped = 0
    for i, obst_loc in enumerate(possible_obstacles):
        if i % 100 == 0:
            print(i)
        new_grid = deepcopy(grid)
        new_grid[obst_loc[0]][obst_loc[1]] = "#"
        new_guard = Guard(new_grid)
        new_guard.go()
        if not new_guard.done:
            looped += 1
    
    print(looped)

