def read_file(input_path):
    return input_path.read_text()


def read_file_as_lines(input_path):
    return read_file(input_path).strip().split("\n")


def read_file_as_grid(input_path, apply_fn=str):
    data = read_file_as_lines(input_path)
    return [[apply_fn(ch) for ch in line] for line in data]
