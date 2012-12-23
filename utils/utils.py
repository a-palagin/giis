__author__ = 'drain'

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


class MinPointsCountError(Exception):
    pass
