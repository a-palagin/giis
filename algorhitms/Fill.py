__author__ = 'drain'


class Fill:

    @staticmethod
    def getPixels(point,pixelsFromScene):
        theStack = [point]
        pixels = []
        while len(theStack)>0:
            pixel = theStack.pop()
            if pixel in pixelsFromScene:
                continue
            pixelsFromScene.append(pixel)
            pixels.append(pixel)
            theStack.append((pixel[0] + 1, pixel[1]))
            theStack.append((pixel[0] - 1, pixel[1]))
            theStack.append((pixel[0], pixel[1] + 1))
            theStack.append((pixel[0], pixel[1] - 1))
        return pixels

class LineFilling:

    @staticmethod
    def getBorders(y, pixelsFromScene):
        borders = []
        for p in pixelsFromScene:
            if p[1] == y:
                borders.append(p)
        borders.sort()
        return borders

    @staticmethod
    def getFillingLine(borders, fillArea):
        line = []
        if len(borders) > 1:
            for i in range(int(borders[0][0]), int(borders[len(borders)-1][0])):
                b = (i, borders[0][1])
                if b in fillArea:
                    line.append(b)
        print("line")
        return line

    @staticmethod
    def getPixels(points, pixelsFromScene):
        uniquePixelsFromScene = []
        for p in pixelsFromScene:
            if p not in uniquePixelsFromScene:
                uniquePixelsFromScene.append(p)
        pixels = []
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
        while minY < maxY:
            minY += 1
            borders = LineFilling.getBorders(minY, uniquePixelsFromScene)
            line = LineFilling.getFillingLine(borders, fillArea)
            pixels.extend(line)
        return pixels