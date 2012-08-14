from tornado.util import ObjectDict


class Map(ObjectDict):
    pass


def cursor_to_dict(cursor, key):
    dct = {}
    for element in cursor:
        dct[element[key]] = element
    return dct
