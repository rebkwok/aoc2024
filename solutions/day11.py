from collections import Counter
from functools import lru_cache

from utils import read_file_as_lines
import math


CACHE = {}

def apply_rule(stone):
    if stone not in CACHE:
        if stone == 0:
            CACHE[stone] = 1,
        else:
            digits = int(math.log10(stone) + 1)
            if digits % 2 == 0:
                num_str = str(stone)
                half = int(digits / 2)
                CACHE[stone] = int(num_str[0:half]), int(num_str[half:])
            else:
                CACHE[stone] = stone * 2024,
    return CACHE[stone]

def apply_rules(stones):
    for stone in stones:
        yield from apply_rule(stone)


def blink(stones, times):
    for i in range(times):
        stones = list(apply_rules(stones))
    return stones


def get_stones(input_path):
    data = read_file_as_lines(input_path)[0]
    return [int(item) for item in data.split()]


def part1(input_path):
    stones = get_stones(input_path)
    new_stones = blink(stones, 25)
    print(len(new_stones))


seen = {}

def add_to_seen(stone, blinks, count):
    if (stone, blinks + 1) not in seen:
        seen[(stone, blinks)] = count
    else:
        seen[(stone, blinks)] = seen[(stone, blinks + 1)] + count


@lru_cache(maxsize=None)
def blink_stone(stone, blinks):
    if blinks == 0:
        return 1

    if stone == 0:
        return blink_stone(1, blinks - 1)
    
    digits = int(math.log10(stone) + 1)
    if digits % 2 == 0:
        num_str = str(stone)
        half = int(digits / 2)
        return blink_stone(int(num_str[0:half]), blinks - 1) + blink_stone(int(num_str[half:]), blinks - 1)
    
    return blink_stone(stone * 2024, blinks - 1)


found = {}


def part2(input_path):
    stones = get_stones(input_path)
    stone_counter = Counter(stones)

    # 0
    # 1
    # 2024
    # 20 24
    # 2 0 2 4


    # for i in range(75):
    #     new_counter = {}
    #     for stone in {**stone_counter}:
    #         new_stones = apply_rule(stone)
    #         count = stone_counter[stone]
    #         for new_stone in new_stones:
    #             new_counter.setdefault(new_stone, 0)
    #             new_counter[new_stone] += count
        
    #     stone_counter = new_counter
   
    # print(sum(stone_counter.values()))

    print(sum(blink_stone(stone, 75) for stone in stones))

