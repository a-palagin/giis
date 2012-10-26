#coding:utf8
__author__ = 'drain'


from PySide import QtGui, QtCore

class GraphicScene(QtGui.QGraphicsScene):
	def __init__(self):
		super(GraphicScene,self).__init__()
		self.__points = []
		self.__gridContainer = []
		self.__pixelSize = 10
		self.setSceneRect(0,0,640,480)
		self.drawGrid()
		self.__pixels = []

	def mousePressEvent(self,event):
		x = event.scenePos().x() - (event.scenePos().x() % self.__pixelSize)
		y = event.scenePos().y() - (event.scenePos().y() % self.__pixelSize)
		if event.button() == QtCore.Qt.LeftButton:
			if self.itemAt(event.scenePos().x(),event.scenePos().y()) in self.__points:
				pass
			else:
				point = self.addEllipse(0, 0, self.__pixelSize, self.__pixelSize)
				point.setBrush(QtGui.QBrush(QtCore.Qt.red))
				point.setZValue(99)
				point.setPos(x,y)
				self.__points.append(point)
		elif event.button() == QtCore.Qt.RightButton:
			if self.itemAt(event.scenePos().x(),event.scenePos().y()) in self.__points:
				point  = self.itemAt(event.scenePos().x(),event.scenePos().y())
				self.removeItem(point)
				self.__points.remove(point)

	def setPixelSize(self, newSize):
		self.__pixelSize = newSize

	def getPixelSize(self):
		return self.__pixelSize

	def drawGrid(self):
		width = int(self.sceneRect().width())
		height = int(self.sceneRect().height())
		if not self.__gridContainer:
			for y in xrange(height/self.__pixelSize+1):
				self.__gridContainer.append(self.addLine(0,y*self.__pixelSize,width,y*self.__pixelSize))
			for x in xrange(width/self.__pixelSize+1):
				self.__gridContainer.append(self.addLine(x*self.__pixelSize,0,x*self.__pixelSize,height))

	def clearEndingPoints(self):
		while len(self.__points):
			self.removeItem(self.__points.pop())
		self.update()

	def clearGrid(self):
		while self.__gridContainer:
			self.removeItem(self.__gridContainer.pop())
		self.update()

	def drawPixel(self,x,y):
		pixel = self.addRect(0,0,self.__pixelSize,self.__pixelSize)
		pixel.setBrush(QtGui.QBrush(QtCore.Qt.black))
		pixel.setPos(x,y)
		self.update()
		self.__pixels.append(pixel)

	def getPixelsOnScene(self):
		return self.__pixels

	def clearSceneFromPixels(self):
		while len(self.__pixels):
			self.removeItem(self.__pixels.pop())
		self.update()

	def getEndingPointsPos(self):
		return [(point.pos().x()/self.__pixelSize,point.pos().y()/self.__pixelSize) for point in self.__points]
