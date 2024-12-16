from argparse import ArgumentParser
from pathlib import Path

from solutions import (
    day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12, day13, 
    day14, day15
)

methods = {
    1: day1,
    2: day2,
    3: day3,
    4: day4,
    5: day5,
    6: day6,
    7: day7,
    8: day8,
    9: day9,
    10: day10,
    11: day11,
    12: day12,
    13: day13,
    14: day14,
    15: day15,
}


def main(day, part, input_path):
    if part == 0:
        print(f"Setting up files for day {day}")
        test_input = input_path / f"day{day}_test.txt"
        real_input = input_path / f"day{day}_input.txt"
        solution_path  = input_path.parent / "solutions" / f"day{day}.py"

        for in_path in [test_input, real_input]:
            if in_path.exists():
                print(f"{in_path} already exists, skipping") 
            else:
                in_path.write_text("")
                print(f"{in_path} created")

        if solution_path.exists():
            print(f"{solution_path} already exists, skipping") 
        else:
            template_path = solution_path.parent / "day_template.py"
            solution_path.write_text(template_path.read_text())
            print(f"{solution_path} created from template; update aoc.py imports")
        return
    if methods.get(day) is None:
        print("Method not found, did you update aoc.py?")
    getattr(methods[day], f"part{part}")(input_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("part", type=int, choices=[0, 1, 2])
    parser.add_argument("-i", "--input-file", type=Path, default=Path(__file__).parent / "input")
    args = parser.parse_args()
    main(args.day, args.part, args.input_file)
