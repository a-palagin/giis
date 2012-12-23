from __future__ import division
__author__ = 'apalagin'


from PySide import QtCore

from utils.utils import singleton, MinPointsCountError
from Scene import GraphicScene
from algorhitms.Line import CDA, Bresenham
from algorhitms.Curve import Bezie, BSpline, Circle, Parabola
from algorhitms.Fill import Fill

@singleton
class SceneManger :
    def __init__(self):
        self.__scene = GraphicScene()
        self.__debugMode = False
        self.__pixelsToDraw = []
        self.__debugTimer = QtCore.QTimer()
        self.__debugTimer.timeout.connect(self.__drawNext)

    def getScene(self):
        return self.__scene

    def setScene(self,scene):
        if isinstance(scene,GraphicScene):
            self.__scene = scene
        raise Exception("must be instance of GraphicScene")

    def setDebugMode(self,mode):
        self.__debugMode = mode

    def isDebugMode(self):
        return self.__debugMode

    def redrawGrid(self):
        self.__scene.clearGrid()
        self.__scene.drawGrid()
        self.__scene.update()

    def setNewPixelSize(self,pixelSize):
        if not pixelSize == self.__scene.getPixelSize():
            self.__scene.setPixelSize(pixelSize)
            self.__scene.clearEndingPoints()
            self.__scene.clearSceneFromPixels()
            self.redrawGrid()

    def getPixelSize(self):
        return self.__scene.getPixelSize()

    def clearAll(self):
        self.__scene.clearEndingPoints()
        self.__scene.clearSceneFromPixels()
        self.__pixelsToDraw = []

    def __drawPixels(self):
        if self.__debugMode:
            self.__debugTimer.start(100)
        else:
            while self.__pixelsToDraw:
                self.__drawNext()

    def __drawNext(self):
        if self.__pixelsToDraw:
            pixel = self.__pixelsToDraw.pop()
            x = round(pixel[0])*self.__scene.getPixelSize()
            y = round(pixel[1])*self.__scene.getPixelSize()
            self.__scene.drawPixel(x,y)
        else:
            self.__debugTimer.stop()

    def drawDDA(self, points = []):
        if not points:
            points =  self.__scene.getEndingPointsPos()
        while len(points) >= CDA.getMinPointsCount():
            self.__pixelsToDraw  += CDA.getPixels(points)
            points.pop(0)
        self.__drawPixels()

    def drawBresenham(self,points = []):
        self.__tmp = []
        if not points:
            points =  self.__scene.getEndingPointsPos()
        while len(points) >= Bresenham.getMinPointsCount():
            self.__tmp += Bresenham.getPixels(points)
            self.__pixelsToDraw += Bresenham.getPixels(points)
            points.pop(0)
        self.__drawPixels()

    def drawCircle(self):
        points =  self.__scene.getEndingPointsPos()
        self.__pixelsToDraw += Circle.getPixels(points)
        self.__drawPixels()

    def drawParabola(self):
        points = self.__scene.getEndingPointsPos()
        self.__pixelsToDraw += Parabola.getPixels(points)
        self.__pixelsToDraw.reverse()
        self.__drawPixels()

    def drawBezie(self):
        points = self.__scene.getEndingPointsPos()
        self.__pixelsToDraw += Bezie.getPixels(points)
        self.__drawPixels()

    def drawBSpline(self):
        points = self.__scene.getEndingPointsPos()
        N = 20
        curve = BSpline.getPixels(points,len(points) - 1,N)
        points = map(curve, (i / N for i in xrange(N + 1)))
        x, y = ([p[j] for p in points] for j in (0, 1))
        keyPoints = zip([round(_x) for _x in x],[round(_y) for _y in y])
        self.drawBresenham(keyPoints)

    def drawFill(self):
        fillPoint = None
        points = self.__scene.getEndingPointsPos()
        if len(points) > 1:
            fillPoint = points.pop()
        points.append(points[0])
        defaultColour = self.__scene.getPixelColour()
        self.drawBresenham(points)
        pixels = Fill.getPixels(fillPoint or points[0],self.__tmp)
        self.__pixelsToDraw += pixels
        self.__scene.setPixelColour(128,0,0)
        self.__drawPixels()
        self.__scene.setPixelColour(*(defaultColour))


