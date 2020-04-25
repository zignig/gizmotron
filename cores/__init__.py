# collection of cores


__all__ = ["pll", "stream","plat","warmboot"]


import os, os.path


def status():
    print(__file__)
    p = os.path.split(__file__)[0]
    print(p)
    li = os.listdir(p)
    for i, j in enumerate(li):
        print(i, j)
