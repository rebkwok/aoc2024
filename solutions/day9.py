from itertools import islice
from utils import read_file_as_lines


def part1(input_path):
    data = read_file_as_lines(input_path)
    assert len(data) == 1
    disk_map = data[0]

    files = [int(num) for num in islice(disk_map, 0, None, 2)]
    free = [int(num) for num in islice(disk_map, 1, None, 2)]
    
    print(list(files))
    print(list(free))

    



def part2():
    ...
