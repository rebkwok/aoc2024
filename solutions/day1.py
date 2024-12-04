from collections import Counter

from utils import read_file, read_file_as_lines


def sorted_lists(input_path):
    input_data = read_file_as_lines(input_path)
    a = []
    b = [] 
    for line in input_data:
        in_a, in_b = line.split()
        a.append(int(in_a.strip()))
        b.append(int(in_b.strip()))
    
    a.sort()
    b.sort()

    return a, b

def part1(input_path):
    a, b = sorted_lists(input_path)
    
    dist = 0
    for (pair_a, pair_b) in zip(a, b):
        dist += abs(pair_a - pair_b)

    print(dist)


def part2(input_path):
    left, right = sorted_lists(input_path)

    right_counter = Counter(right)

    similarity = 0

    for num in left:
        similarity += num * right_counter.get(num, 0)
    
    print(similarity)

