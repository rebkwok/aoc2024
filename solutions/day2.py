from utils import read_file_as_lines


def _test(test1, test2):
    diff_from_prev = test1 - test2
    return (diff_from_prev <= 3 and diff_from_prev >= 1)


def _test_inc(level):
    for i in range(1, len(level)):
        if not _test(level[i], level[i - 1]):
            return False
    return True


def _test_dec(level):
    for i in range(1, len(level)):
        if not _test(level[i - 1], level[i]):
            return False
    return True


def part1(input_path):
    levels = [[int(lev_it) for lev_it in lev.split()] for lev in read_file_as_lines(input_path)]

    safe_levels = 0
    for level in levels:
        if level[0] == level[1]:
            safe = False
        elif level[1] > level[0]:
            safe = _test_inc(level)
        else:
            safe = _test_dec(level)

        if safe:
            safe_levels += 1
    
    print(safe_levels)



def test_level(level):
    if level[0] == level[1]:
        return False
    if level[1] > level[0]:
        return _test_inc(level)
    return _test_dec(level)



def part2(input_path):
    levels = [[int(lev_it) for lev_it in lev.split()] for lev in read_file_as_lines(input_path)]

    safe_levels = 0
    for level in levels:
        safe = test_level(level)
        if not safe:
            for i in range(len(level)):
                new_level = [it for j, it in enumerate(level) if j != i]
                safe = test_level(new_level)
                if safe:
                    break

        if safe:
            safe_levels += 1
    
    print(safe_levels)
