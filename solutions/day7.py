from itertools import product, zip_longest, chain
import re
from utils import read_file_as_lines


EQ_REG = re.compile(r"^(?P<test>\d+):(?P<numbers>(?P<number>\s\d+)+)")

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def concat(a, b):
    return int(str(a) + str(b))

def parse_equation(equation, operators):
    matched = EQ_REG.match(equation)
    test = int(matched.group("test"))
    numbers = [int(num.strip()) for num in matched.group("numbers").strip().split()]
    operator_combinations = product(operators, repeat=len(numbers) - 1)
    return (test, numbers, operator_combinations)


def can_match(equation):
    test_value, numbers, possible_operators = equation

    for operators in possible_operators:
        number_test = numbers[1:]
        result = numbers[0]
        for i, operator in enumerate(operators):
            result = operator(result, number_test[i])
            if result > test_value:
                continue
        if result == test_value:
            return True
    return False
    

def get_total(equations):
    tally = 0

    for equation in equations:
        if can_match(equation):
            tally += equation[0]
    
    return tally


def part1(input_path):
    data = read_file_as_lines(input_path)
    equations = [parse_equation(equation, [add, multiply]) for equation in data]

    print(get_total(equations))


def part2(input_path):
    data = read_file_as_lines(input_path)
    equations = [parse_equation(equation, [add, multiply, concat]) for equation in data]

    print(get_total(equations))
