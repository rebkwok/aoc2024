import re

from utils import read_file, read_file_as_lines

instr_re = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
instr_re = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

def get_result(string):
    found = instr_re.findall(string)
    
    result = 0
    for (a, b) in found:
        result += int(a) * int(b)
    return result

def part1(input_path):
    data = read_file(input_path)
    result = get_result(data) 
    print(result)


def part2(input_path):
    data = read_file_as_lines(input_path)
    data = "".join(data)

    # get start of string up to the first do() or don't() instruction
    start = re.findall(r"^(.*?mul\(\d{1,3},\d{1,3}\).*?)?(?:(?:do\(\))|(?:don't\(\)))", data)

    # remove start from the string
    data = data.replace(start[0], '', 1)

    # now find all commands that are either between a do() and a don't() or between a
    # do() and the end 
    all_dos = re.findall(r"do\(\)(.*?mul\(\d{1,3},\d{1,3}\).*?)(?:don't\(\)|$)", data)

    result = 0
    for do_str in start + all_dos:
        result += get_result(do_str)
    print(result)
