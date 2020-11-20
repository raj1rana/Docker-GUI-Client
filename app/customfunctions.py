from collections import namedtuple


def customDecoder(Dict):
    return namedtuple('X', Dict.keys())(*Dict.values())
