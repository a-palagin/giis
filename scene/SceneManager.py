__author__ = 'apalagin'

import time

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
		points =  self.__scene.getEndingPointsPos()
		pixels = Line.CDA(points)
		for pixel in pixels:
			x = round(pixel[0])*self.__scene.getPixelSize()
			y = round(pixel[1])*self.__scene.getPixelSize()
			self.__scene.drawPixel(x,y)
			if self.__debugMode:
				time.sleep(0.01)

	def drawBresenham(self):
		points =  self.__scene.getEndingPointsPos()
		pixels = Line.Bresenham(points)
		for pixel in pixels:
			x = round(pixel[0])*self.__scene.getPixelSize()
			y = round(pixel[1])*self.__scene.getPixelSize()
			self.__scene.drawPixel(x,y)
			if self.__debugMode:
				time.sleep(0.01)

	def drawCurve(self):
		first,last = self.__scene.getEndingPointsPos()
		pixelSize = self.__scene.getPixelSize()
		pixels = Curve.Bresenham(first.x()/pixelSize,first.y()/pixelSize,last.x()/pixelSize,last.y()/pixelSize)
		for pixel in pixels:
			x = round(pixel[0])*pixelSize
			y = round(pixel[1])*pixelSize
			self.__scene.drawPixel(x,y)
			if self.__debugMode:
				time.sleep(0.01)


