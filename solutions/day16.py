import heapq

from collections import defaultdict

from utils import read_file_as_grid


def get_next_positions(maze, visited, pos, current_direction):
    # next possible positions are one of 4 if not in seen
    # and not #
    r, c = pos
    possible_positions = {
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1)
    }
    possible_positions -= visited
    match current_direction:
        case "N":
            possible_positions -= {(r + 1, c)}
        case "S":
            possible_positions -= {(r - 1, c)}
        case "W":
            possible_positions -= {(r, c + 1)}
        case "E":
            possible_positions -= {(r, c - 1)}

    for r_pos, c_pos in possible_positions:
        if maze[r_pos][c_pos] not in ["#", "%"]:
            yield (r_pos, c_pos)


def move(from_pos, to_pos, current_direction):
    # score 1 for moving forwards
    cost = 1

    # Do we need to also rotate?
    if to_pos[0] < from_pos[0]:
        direction = "N"
    elif to_pos[0] > from_pos[0]:
        direction = "S"
    elif to_pos[1] < from_pos[1]:
        direction = "W"
    else:
        assert to_pos[1] > from_pos[1]
        direction = "E"

    if direction == current_direction:
        return direction, cost
    else:
        return direction, cost + 1000


def manhattan_dist(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(maze, starting_position, starting_direction, end_position, exclude=[]):
    queue = []
    heapq.heappush(queue, (0, starting_position, starting_direction))

    came_from = {starting_position: None}
    cost_so_far = {starting_position: 0}

    while queue:

        current_priority, current_position, current_direction = heapq.heappop(queue)

        if current_position == end_position:
            break

        next_positions = get_next_positions(maze, set(), current_position, current_direction)
        for next_position in next_positions:
            new_direction, cost = move(current_position, next_position, current_direction)
            new_cost = cost_so_far[current_position] + cost
            if next_position not in exclude:
                if next_position not in cost_so_far or new_cost < cost_so_far[next_position]:
                    cost_so_far[next_position] = new_cost
                    priority = new_cost + manhattan_dist(end_position, next_position)
                    heapq.heappush(queue, (priority, next_position, new_direction))
                    came_from[next_position] = current_position

    return came_from, cost_so_far




def a_star_all(maze, starting_position, starting_direction, end_position):
    queue = []
    heapq.heappush(queue, (0, starting_position, starting_direction, 0))

    cost_at_point = {(starting_position, starting_direction): 0}

    visited = set([(starting_position, starting_direction)]) 
    parents = defaultdict(list) 
 
    parents[starting_position] = []
    lowest_cost = None
    found = []
    
    while queue:

        current_priority, current_position, current_direction, current_cost = heapq.heappop(queue)

        if current_position == end_position:
            found.append((end_position, current_cost))
            
        else:
            next_positions = get_next_positions(maze, set(), current_position, current_direction)

            for next_position in next_positions:
                next_direction, cost = move(current_position, next_position, current_direction)
                new_cost = current_cost + cost

                # if (next_position, next_direction) not in cost_at_point or new_cost < cost_at_point[(next_position, next_direction)]:
                if (next_position, next_direction) not in visited:
                    visited.add((next_position, next_direction)) 
                    cost_at_point[(next_position, next_direction)] = new_cost
                    priority = new_cost + manhattan_dist(end_position, next_position)
                    heapq.heappush(queue, (priority, next_position, next_direction, new_cost))
                    parents[next_position].append((current_position, new_cost))
                elif found:
                    parents[next_position].append((current_position, new_cost))

    # If no path found 
    if not found: 
        return [] 

    # Function to backtrack and find all paths 
    def backtrack_paths(node, current_cost): 
        if node == starting_position: 
            return [[starting_position]] 
        paths = [] 
        for (p, node_cost) in parents[node]: 
            if node_cost <= current_cost:
                for path in backtrack_paths(p, node_cost): 
                    paths.append(path + [node]) 
        return paths 
    
    lowest_cost = min(p[1] for p in parents[end_position])
    return lowest_cost, backtrack_paths(end_position, lowest_cost)


def part1(input_path):
    maze = read_file_as_grid(input_path)

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "S":
                current_position = (i, j)
            if maze[i][j] == "E":
                end_position = (i, j)
    current_direction = "E"

    came_from, cost_so_far = a_star(maze, current_position, current_direction, end_position)
    print(cost_so_far[end_position])


def part2(input_path):
    maze = read_file_as_grid(input_path)

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "S":
                current_position = (i, j)
            if maze[i][j] == "E":
                end_position = (i, j)
    current_direction = "E"

    lowest_cost, paths = a_star_all(maze, current_position, current_direction, end_position)

    for path in paths:
        direction = current_direction
        cost = 0
        current_r, current_c = current_position
        for next_point in path[1:]:
            move_direction, move_cost = move((current_r, current_c), next_point, direction)
            cost += move_cost
            current_r, current_c = next_point
            direction = move_direction
        assert cost == lowest_cost

    print(lowest_cost)
    print(len(set(sum(paths, []))))
