from argparse import ArgumentParser
from pathlib import Path

from solutions import day1, day2, day3, day4, day5

methods = {
    1: day1,
    2: day2,
    3: day3,
    4: day4,
    5: day5,
    6: None,
    7: None,
    8: None,
    9: None,
    10: None,
    11: None,
    12: None,
    13: None,
    14: None,
    15: None,
}


def main(day, part, input_path):
    getattr(methods[day], f"part{part}")(input_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("part", type=int, choices=[1, 2])
    parser.add_argument("input_file", type=Path)
    args = parser.parse_args()
    main(args.day, args.part, args.input_file)
