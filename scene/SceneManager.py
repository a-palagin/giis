__author__ = 'apalagin'

import time

from PySide import QtCore

from Scene import GraphicScene
from algorhitms.Line import Line
from algorhitms.Curve import Curve

def singleton(cls):
	instances = {}
	def getinstance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return getinstance

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

	def drawDDA(self):
		self.__pixelsToDraw = []
		points =  self.__scene.getEndingPointsPos()
		self.__pixelsToDraw  = Line.CDA(points)
		self.__drawPixels()

	def drawBresenham(self):
		self.__pixelsToDraw = []
		points =  self.__scene.getEndingPointsPos()
		self.__pixelsToDraw = Line.Bresenham(points)
		self.__drawPixels()

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

	def drawCurve(self):
		self.__pixelsToDraw = []
		points =  self.__scene.getEndingPointsPos()
		self.__pixelsToDraw = Curve.threePointsCircle(points)

