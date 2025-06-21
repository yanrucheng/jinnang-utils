def list_to_tuple(my_type):
    def convert(l):
        return tuple(my_type(x) for x in l)
    return convert


def get_first_value(d, keys, default=None):
    for key in keys:
        val = d.get(key)
        if val is not None and val != '':
            return val
    return default