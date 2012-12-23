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
