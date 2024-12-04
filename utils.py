def read_file(input_path):
    return input_path.read_text()


def read_file_as_lines(input_path):
    return read_file(input_path).strip().split("\n")
