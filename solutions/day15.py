from copy import deepcopy
from utils import read_file_as_lines


def get_next_space(map, robot_position, direction):
    space = None
    original_robot_row, original_robot_col = robot_position
    new_robot_position = robot_position
    match direction:
        case "<":
            robot_c = robot_position[1]
            while robot_c >= 0:
                robot_c -= 1
                if map[original_robot_row][robot_c] == "#":
                    break
                elif map[original_robot_row][robot_c] == ".":
                    space = (original_robot_row, robot_c)
                    new_robot_position = (original_robot_row,  robot_position[1] - 1)
                    break
        case ">":
            robot_c = robot_position[1]
            while robot_c < len(map[0]):
                robot_c += 1
                if map[original_robot_row][robot_c] == "#":
                    break
                elif map[original_robot_row][robot_c] == ".":
                    space = (original_robot_row, robot_c)
                    new_robot_position = (original_robot_row,  robot_position[1] + 1)
                    break
        case "^":
            robot_r = robot_position[0]
            while robot_r >= 0:
                robot_r -= 1
                if map[robot_r][original_robot_col] == "#":
                    break
                elif map[robot_r][original_robot_col] == ".":
                    space = (robot_r, original_robot_col)
                    new_robot_position = (robot_position[0] - 1, original_robot_col)
                    break
        case "v":
            robot_r = robot_position[0]
            while robot_r < len(map):
                robot_r += 1
                if map[robot_r][original_robot_col] == "#":
                    break
                elif map[robot_r][original_robot_col] == ".":
                    space = (robot_r, original_robot_col)
                    new_robot_position = (robot_position[0] + 1, original_robot_col)
                    break
    return space, new_robot_position

    
def move(map, robot_position, direction):
    """
    Find row (L/R) or column (U/D) from direction
    From robots position, find the position of the next "." in the specified direction, ignoring
    "O"'s
    If there is one, move the robot and all the Os between the robot's position and the . one unit
    """
    original_robot_row, original_robot_col = robot_position
    space, new_robot_position = get_next_space(map, robot_position, direction)
    if space:
        # update map
        # 1) replace current robot position with "."
        # 2) replace current robot position +1 with robot
        # 3) if space != current robot position +1, replace space and for every position between new robot position and space with O
        map[robot_position[0]][robot_position[1]] = "."
        map[new_robot_position[0]][new_robot_position[1]] = "@"
        
        if space != new_robot_position:
            match direction:
                case "<":
                    for i in range(new_robot_position[1] - 1, space[1] -1, -1):
                        map[original_robot_row][i] = "O"
                case ">":
                    for i in range(new_robot_position[1] + 1, space[1] + 1):
                        map[original_robot_row][i] = "O"
                case "^":
                    for i in range(new_robot_position[0] - 1, space[0] -1, -1):
                        map[i][original_robot_col] = "O"
                case "v":
                    for i in range(new_robot_position[0] + 1, space[0] + 1):
                        map[i][original_robot_col] = "O"

    return map, new_robot_position


def can_move(robot_map, robot_position, direction):
    new_robot_position = robot_position
    original_robot_row, original_robot_col = robot_position
    blocks_to_move = set()

    match direction:
        case  "^":
            new_robot_position =  (original_robot_row - 1, original_robot_col)
            # is the 1 above empty; if so, we can move and we're done
            if robot_map[original_robot_row - 1][original_robot_col] == ".":
                return True, new_robot_position, blocks_to_move
            # is the 1 above a wall; if so, we can't move and we're done
            if robot_map[original_robot_row - 1][original_robot_col] == "#":
                return False, robot_position, blocks_to_move
            
            # the 1 above is part of a block, [ or ]
            queue = [robot_position]
            moves = set()
            can_move = True
            while queue:
                pos = queue.pop()
                r, c = pos
                if robot_map[r -1][c] == "#":
                    can_move = False
                    break
                elif robot_map[r -1][c] == "[":
                    queue.append((r - 1, c))
                    queue.append((r - 1, c + 1))
                    moves.add((r, c))
                elif robot_map[r -1][c] == "]":
                    queue.append((r - 1, c))
                    queue.append((r - 1, c - 1))
                    moves.add((r, c))
                elif robot_map[r -1][c] == ".":
                    moves.add((r, c))
            if not can_move:
                return False, robot_position, blocks_to_move
            moves = moves - {robot_position}
            return True, new_robot_position, moves

        case "v":
            new_robot_position = (original_robot_row + 1, original_robot_col)
            # is the 1 below empty; if so, we can move and we're done
            if robot_map[original_robot_row + 1][original_robot_col] == ".":
                return True, new_robot_position, blocks_to_move
            # is the 1 below a wall; if so, we can't move and we're done
            if robot_map[original_robot_row + 1][original_robot_col] == "#":
                return False, robot_position, blocks_to_move
            
            # the 1 below is part of a block, [ or ]
            queue = [robot_position]
            moves = set()
            can_move = True
            while queue:
                pos = queue.pop()
                r, c = pos
                if robot_map[r + 1][c] == "#":
                    can_move = False
                    break
                elif robot_map[r + 1][c] == "[":
                    queue.append((r + 1, c))
                    queue.append((r + 1, c + 1))
                    moves.add((r, c))
                elif robot_map[r + 1][c] == "]":
                    queue.append((r + 1, c))
                    queue.append((r + 1, c - 1))
                    moves.add((r, c))
                elif robot_map[r + 1][c] == ".":
                    moves.add((r, c))
            if not can_move:
                return False, robot_position, blocks_to_move
            moves = moves - {robot_position}
            return True, new_robot_position, moves
            

def print_map(map):
    for r in map:
        print("".join(r))
    print("")


def move2(robot_map, robot_position, direction):
    """
    Find row (L/R) or column (U/D) from direction
    From robots position, find the position of the next "." in the specified direction, ignoring
    "[]"'s
    If there is one, move the robot and all the []s between the robot's position and the . one unit
    """
    original_robot_row, original_robot_col = robot_position
    new_robot_position = robot_position

    if direction in ["<", ">"]:
        space, new_robot_position = get_next_space(robot_map, robot_position, direction)
        if space:
            # update map
            # 1) replace current robot position with "."
            # 2) replace current robot position +1 with robot
            # 3) if space != current robot position +1
            # replace space and for every position between new robot position and space with O
            robot_map[robot_position[0]][robot_position[1]] = "."
            robot_map[new_robot_position[0]][new_robot_position[1]] = "@"
            
            if space != new_robot_position:
                match direction:
                    case "<":
                        for i in range(new_robot_position[1] - 1, space[1] -1, -1):
                            if (new_robot_position[1] - 1 - i) % 2 == 0:
                                robot_map[original_robot_row][i] = "]"
                            else:
                                robot_map[original_robot_row][i] = "["
                    case ">":
                        for i in range(new_robot_position[1] + 1, space[1] + 1):
                            if (new_robot_position[1] + 1 + i) % 2 == 0:
                                robot_map[original_robot_row][i] = "["
                            else:
                                robot_map[original_robot_row][i] = "]"

    else:
        move_allowed, new_robot_position, blocks_to_move = can_move(robot_map, robot_position, direction)
        map_copy = deepcopy(robot_map)
        if move_allowed:
            if direction == "^":
                for block in sorted(blocks_to_move):
                    map_copy[block[0]][block[1]] = "."
                    map_copy[block[0] - 1][block[1]] = robot_map[block[0]][block[1]]
            else:
                for block in sorted(blocks_to_move, reverse=True):
                    map_copy[block[0]][block[1]] = "."
                    map_copy[block[0] + 1][block[1]] = robot_map[block[0]][block[1]]

            map_copy[robot_position[0]][robot_position[1]] = "."
            map_copy[new_robot_position[0]][new_robot_position[1]] = "@"
            robot_map = map_copy

    return robot_map, new_robot_position


def map_coords(map, token="O"):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == token:
                yield 100 * i + j

def get_map_and_instructions(input_path):
    data = read_file_as_lines(input_path)
    map = []
    instructions = ""

    for row in data:
        if not row:
            continue
        if row.startswith("#"):
            map.append(row)
        else:
            instructions += row

    map = [[pos for pos in row] for row in map]
    return map, instructions


def part1(input_path):
    map, instructions = get_map_and_instructions(input_path)
    robot_position = next((r, c) for r in range(len(map)) for c in range(len(map[0])) if map[r][c] == "@")

    for r in map:
        print("".join(r))
    print("")

    for instruction in instructions:
        map, robot_position = move(map, robot_position, instruction)

    for r in map:
        print("".join(r))
    print("")
    print(sum(list(map_coords(map))))


def part2(input_path):
    original_map, instructions = get_map_and_instructions(input_path)

    robot_map = [[] for row in original_map]

    for row in range(len(original_map)):
        for col in range(len(original_map[0])):
            original_val = original_map[row][col]
            if original_val == "O":
                robot_map[row].append("[")
                robot_map[row].append("]")
            elif original_val == "@":
                robot_map[row].append("@")
                robot_map[row].append(".")
            else:
                for i in range(2):
                    robot_map[row].append(original_val)

    robot_position = next((r, c) for r in range(len(robot_map)) for c in range(len(robot_map[0])) if robot_map[r][c] == "@")

    for instruction in instructions:
        robot_map, robot_position = move2(robot_map, robot_position, instruction)
    # print_map(robot_map)
    print(sum(list(map_coords(robot_map, token="["))))
