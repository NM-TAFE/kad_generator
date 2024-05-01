def add_tuples(*arg):
    return tuple(map(sum, zip(*arg)))
