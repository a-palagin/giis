__author__ = 'apalagin'

from Scene import GraphicScene
from algorhitms.Line import Line

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

	def getScene(self):
		return self.__scene

	def setScene(self,scene):
		if isinstance(scene,GraphicScene):
			self.__scene = scene
		raise Exception("must be instance of GraphicScene")

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

	def drawCDA(self):
		first,last = self.__scene.getEndingPointsPos()
		pixelSize = self.__scene.getPixelSize()
		pixels = Line.CDA(first.x()/pixelSize,first.y()/pixelSize,last.x()/pixelSize,last.y()/pixelSize)
		for pixel in pixels:
			self.__scene.drawPixel(round(pixel[0])*pixelSize,round(pixel[1])*pixelSize)

	def drawBresenham(self):
		first,last = self.__scene.getEndingPointsPos()
		pixelSize = self.__scene.getPixelSize()
		pixels = Line.Bresenham(first.x()/pixelSize,first.y()/pixelSize,last.x()/pixelSize,last.y()/pixelSize)
		for pixel in pixels:
			self.__scene.drawPixel(round(pixel[0])*pixelSize,round(pixel[1])*pixelSize)
