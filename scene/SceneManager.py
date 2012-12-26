from __future__ import division
__author__ = 'apalagin'


from PySide import QtCore

from utils.utils import singleton, MinPointsCountError, convert, Colors
from Scene import GraphicScene
from algorhitms.Line import CDA, Bresenham
from algorhitms.Curve import Bezie, BSpline, Circle, Parabola
from algorhitms.Fill import Fill, LineFilling
from algorhitms.Amputation import Amputation

@singleton
class SceneManger :
    def __init__(self):
        self.__scene = GraphicScene()
        self.__debugMode = False
        self.__pixelsToDraw = []
        self.__pixelsOnScene = []
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
        self.__pixelsOnScene = []

    def __drawPixels(self):
        if self.__debugMode:
            self.__debugTimer.start(100)
        else:
            while self.__pixelsToDraw:
                self.__drawNext()

    def __drawNext(self):
        if self.__pixelsToDraw:
            pixel = self.__pixelsToDraw.pop()
            pixel.x = round(pixel.x)*self.__scene.getPixelSize()
            pixel.y = round(pixel.y)*self.__scene.getPixelSize()
            self.__scene.drawPixel(pixel)
        else:
            self.__debugTimer.stop()

    def drawDDA(self, points = []):
        if not points:
            points =  self.__scene.getEndingPointsPos()
        while len(points) >= CDA.getMinPointsCount():
            self.__pixelsToDraw  += convert(CDA.getPixels(points))
            points.pop(0)
        self.__drawPixels()

    def drawBresenham(self,points = []):
        self.__tmp = []
        if not points:
            points =  self.__scene.getEndingPointsPos()
        while len(points) >= Bresenham.getMinPointsCount():
            self.__tmp += Bresenham.getPixels(points)
            self.__pixelsToDraw += convert(Bresenham.getPixels(points))
            points.pop(0)
        self.__drawPixels()

    def drawCircle(self):
        points =  self.__scene.getEndingPointsPos()
        self.__pixelsToDraw += convert(Circle.getPixels(points))
        self.__drawPixels()

    def drawParabola(self):
        points = self.__scene.getEndingPointsPos()
        self.__pixelsToDraw += convert(Parabola.getPixels(points))
        self.__pixelsToDraw.reverse()
        self.__drawPixels()

    def drawBezie(self):
        points = self.__scene.getEndingPointsPos()
        self.__pixelsToDraw += convert(Bezie.getPixels(points))
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
        self.drawBresenham(points)
        pixels = Fill.getPixels(fillPoint or points[0],self.__tmp)
        self.__pixelsToDraw += convert(pixels, color=Colors.blue)
        self.__pixelsToDraw.reverse()
        self.__drawPixels()

    def drawLineFilling(self):
        points = self.__scene.getEndingPointsPos()
        vertexes = list(points)
        points.append(points[0])
        self.drawBresenham(points)
        pixels = LineFilling.getPixels(vertexes, self.__tmp)
        self.__pixelsToDraw += convert(pixels, color=Colors.blue)
        self.__pixelsToDraw.reverse()
        self.__drawPixels()

    def drawAmputatedLine(self, points = []):
        self.__tmp = []
        if not points:
            points =  self.__scene.getEndingPointsPos()
        while len(points) >= Bresenham.getMinPointsCount():
            self.__tmp += Bresenham.getPixels(points)
            pixels = Amputation.setPixelVisibility(self.__tmp)
            self.__pixelsToDraw += pixels
            self.__pixelsToDraw.reverse()
            points.pop(0)
        self.__drawPixels()

    def drawVisibleArea(self):
        points = self.__scene.getEndingPointsPos()
        vertexes = list(points)
        points.append(points[0])
        self.drawBresenham(points)
        Amputation.getVisibleArea(vertexes, self.__tmp)