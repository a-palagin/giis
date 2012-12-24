__author__ = 'drain'

class Color:

    def __init__(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue


class Colors:

    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)
    black = Color(0,0,0)
    white = Color(255,255,255)


class Pixel:

    def __init__(self,x, y, color=Colors.black):
        self.x = x
        self.y = y
        self.color = color


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

def convert(listOfPixels, color = Colors.black):
    tmp = []
    for pixel in listOfPixels:
        tmp.append(Pixel(*pixel,color = color))
    return tmp


class MinPointsCountError(Exception):
    pass
