import re
import numpy
from dataclasses import dataclass
from utils import read_file_as_lines


BUTTON_RE = re.compile(r".+X\+(?P<x>\d+), Y\+(?P<y>\d+)")
PRIZE_RE = re.compile(r".+X=(?P<x>\d+), Y=(?P<y>\d+)")

@dataclass
class Button:
    x: int
    y: int
    tokens: int

    @classmethod
    def parse(cls, data, tokens):
        matches = BUTTON_RE.match(data)
        return cls(
            x=int(matches.group("x")),
            y=int(matches.group("y")),
            tokens=tokens
        )


@dataclass
class Prize:
    x: int
    y: int

    @classmethod
    def parse(cls, data, conversion):
        matches = PRIZE_RE.match(data)
        return cls(
            x=int(matches.group("x")) + conversion,
            y=int(matches.group("y")) + conversion,
        )


@dataclass
class Machine:
    a: Button
    b: Button
    prize: Prize

    @classmethod
    def parse(cls, data, conversion):
        a, b, prize = data
        return cls(
            a=Button.parse(a, 3),
            b=Button.parse(b, 1),
            prize=Prize.parse(prize, conversion)
        )
    
    def calculate_score(self):
        buttons = numpy.array([[self.a.x, self.b.x], [self.a.y, self.b.y]])
        prize = numpy.array([self.prize.x, self.prize.y])
        inv_buttons = numpy.linalg.inv(buttons)
        solution = numpy.dot(inv_buttons, prize)
        presses = [round(sol) for sol in solution]
        if self.wins(*presses):
            return presses[0] * self.a.tokens + presses[1] * self.b.tokens
        return 0

    def calculate(self, a_presses, b_presses):
        return a_presses * self.a.x + b_presses * self.b.x, a_presses * self.a.y + b_presses * self.b.y

    def wins(self, a_presses, b_presses):
        return self.calculate(a_presses, b_presses) == (self.prize.x, self.prize.y)


def get_machines(input_path, conversion=0):
    data = read_file_as_lines(input_path)
    machines = []
    current_machine = []
    for line in data:
        if not line:
            machines.append(Machine.parse(current_machine, conversion=conversion))
            current_machine = []
            continue
        current_machine.append(line)
    machines.append(Machine.parse(current_machine, conversion=conversion))
    return machines


def part1(input_path):
    machines = get_machines(input_path)
    tokens_used = sum(machine.calculate_score() for machine in machines) 
    print(tokens_used)


def part2(input_path):
    machines = get_machines(input_path, conversion=10000000000000)
    tokens_used = sum(machine.calculate_score() for machine in machines) 
    print(tokens_used)
