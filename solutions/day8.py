from utils import read_file_as_grid


def part1(input_path, incl_resonate_freq=False):
    rows = read_file_as_grid(input_path)

    row_count = len(rows)
    col_count = len(rows[0])
    antennae = {}
    for i in range(row_count):
        for j in range(col_count):
            val = rows[i][j]
            if val != ".":
                antennae.setdefault(val, []).append((i, j))
    
    def in_grid(pos):
        return (0 <= pos[0] < row_count) and (0 <= pos[1] < col_count)

    antinodes = set()
    for a, positions in antennae.items():
        for i, pos in enumerate(positions):
            for other_pos in positions[i + 1:]:
                x_diff, y_diff = pos[0] - other_pos[0], pos[1] - other_pos[1]
                
                locs = [(pos[0] + x_diff, pos[1] + y_diff), (other_pos[0] - x_diff, other_pos[1] - y_diff)]

                if incl_resonate_freq:
                    antinodes.add(pos)
                    antinodes.add(other_pos)

                    pos1 = locs[0]
                    pos2 = locs[1]

                    while in_grid(pos1) or in_grid(pos2):
                        pos1 = (pos1[0] + x_diff, pos1[1] + y_diff)
                        pos2 = (pos2[0] - x_diff, pos2[1] - y_diff)              
                        locs.extend([pos1, pos2])      

                for loc in locs:
                    if in_grid(loc):
                        antinodes.add(loc)

    print(len(set(antinodes)))
            

def part2(input_path):
    part1(input_path, incl_resonate_freq=True)

    

