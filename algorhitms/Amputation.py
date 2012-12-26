__author__ = 'Raphanum'

from algorhitms.Fill import Fill, LineFilling
from utils.utils import singleton, MinPointsCountError, convert, Colors


class Amputation:

    visibleArea = []

    @staticmethod
    def getVisibleArea(points, pixelsFromScene):
        maxY = minY = points[0][1]
        maxX = minX = points[0][0]
        for p in points:
            if maxY < p[1]:
                maxY = p[1]
            elif minY > p[1]:
                minY = p[1]
            if maxX < p[0]:
                maxX = p[0]
            elif minX > p[0]:
                minX = p[0]
        fillPoint = (round((minX + maxX)/2), round((minY + maxY)/2))
        fillArea = Fill.getPixels(fillPoint, pixelsFromScene)
        Amputation.visibleArea = fillArea

    @staticmethod
    def setPixelVisibility(points):
        pixels = []
        firstInvPixels = []
        lastInvPixels = []
        visiblePixels = []
        if points[0] in Amputation.visibleArea:
            for p in points:
                if p in Amputation.visibleArea:
                    visiblePixels.append(p)
                else:
                    lastInvPixels.append(p)
        else:
            i = 0
            for p in points:
                if p in Amputation.visibleArea:
                    i = 1
                    visiblePixels.append(p)
                elif i < 1:
                    firstInvPixels.append(p)
                else:
                    lastInvPixels.append(p)
        pixels += convert(firstInvPixels)
        pixels += convert(visiblePixels, color=Colors.green)
        pixels += convert(lastInvPixels)
        return pixels
