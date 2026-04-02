import sys

Error_TYPE = {
    1: "TypeError",
    2: 'SyntaxError',
    3: 'NameError',
    4: 'SQLError',
    5: 'ModuleNotFoundError',
    6: 'AttributeError',
    1000: 'UnknownError',
}

def errException(error_index : int, text :str, pgCounter : int, line : str):
    print(file=sys.stderr)
    print(f"{Error_TYPE[error_index]} :  {text}   ", file=sys.stderr)
    print(file=sys.stderr)
    print(f"  \" {line} \"  --- line : {pgCounter}  ", file=sys.stderr)
    print(' ', '~' * (len(line) + 4), file=sys.stderr)
    sys.exit()