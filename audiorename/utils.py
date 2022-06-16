import re


def indent(text: str) -> str:
    return '    ' + re.sub(r'\n', '\n    ', text)


def read_file(path: str) -> str:
    return open(path, 'r').read()
