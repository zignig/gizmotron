# registration decorator


available = {}


def register(cls):
    available[cls.__name__] = cls
    return cls


def show():
    return available
