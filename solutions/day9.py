from dataclasses import dataclass
from itertools import islice, zip_longest
from utils import read_file_as_lines


def checksum(diskmap):
    tally = 0
    for i in range(len(diskmap)):
        tally += (i * int(diskmap[i]))

    return tally


def part1(input_path):
    data = read_file_as_lines(input_path)
    disk_map = data[0]

    files = [[str(i)] * int(num) for i, num in enumerate(islice(disk_map[2:], 0, None, 2), start=1)]            
    
    new_map = sum([["0"] * int(disk_map[0])], [])
    free = [int(num) for num in islice(disk_map, 1, None, 2)]

    for spaces in free:
        if not files:
            break
        for i in range(spaces):
            if not files:
                break
            new_map.append(files[-1].pop())
            if not files[-1]:
                files = files[:-1]

        if not files:
            break
        new_map.extend(files[0])
        files = files[1:]
            
    print(checksum(new_map))


def part2(input_path):
    data = read_file_as_lines(input_path)
    disk_map = data[0]

    # id (or 0 for space), size for each block
    disk_map = [
        (i//2 if i % 2 == 0 else 0, int(num)) for i, num in enumerate(disk_map)]
    
    # Go backwards through disk map for files
    # and forwards up to the location of the current file for spaces
    # (from 1, as 0 has id 0, which is the same as a space id)
    for file_ix in range((len(disk_map) -1), 0, -1):
        for space_ix in range(1, file_ix):
            file_id, file_size = disk_map[file_ix]
            space_id, space_size = disk_map[space_ix]

            # ignore if file_id is 0, it's a space, we don't move those around
            if file_id and not space_id and file_size <= space_size:
                # update file to empty
                disk_map[file_ix] = (0, file_size)
                # update space
                disk_map[space_ix] = (0, space_size - file_size)
                # insert file before space
                disk_map.insert(space_ix, (file_id, file_size))
    
    disk_map = [block for block in disk_map if block[1] > 0]
    
    first = [disk_map[0][0]] * disk_map[0][1]
    disk_map = [
        [block_id] * block_size for (block_id, block_size) in  
        disk_map[1:]
    ]
    disk_map = sum([first, *disk_map], [])
    print(checksum(disk_map))

