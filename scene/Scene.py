#coding:utf8
__author__ = 'drain'


from PySide import QtGui, QtCore

class GraphicScene(QtGui.QGraphicsScene):
	def __init__(self):
		super(GraphicScene,self).__init__()
		self.__firstPoint  = None #QtGui.QGraphicsEllipseItem()
		self.__lastPoint  = None #QtGui.QGraphicsEllipseItem()
		self.__gridContainer = []
		self.__pixelSize = 10
		self.setSceneRect(0,0,640,480)
		self.drawGrid()
		self.__pixels = []

	def mouseDoubleClickEvent(self,event):
		x = event.scenePos().x() - (event.scenePos().x() % self.__pixelSize)
		y = event.scenePos().y() - (event.scenePos().y() % self.__pixelSize)
		if not self.__firstPoint:
			self.__firstPoint = self.addEllipse(0, 0, self.__pixelSize, self.__pixelSize)
			self.__firstPoint.setBrush(QtGui.QBrush(QtCore.Qt.red))
			#и этот тоже
			self.__firstPoint.setPos(x, y)
		elif self.__lastPoint:
			self.__lastPoint.setPos(x, y)
		else:
			self.__lastPoint = self.addEllipse(0,0,self.__pixelSize,self.__pixelSize)
			self.__lastPoint.setBrush(QtGui.QBrush(QtCore.Qt.blue))
			#адовый пиздец
			self.__lastPoint.setPos(x, y)

	def mousePressEvent(self,event):
		if event.button() == QtCore.Qt.RightButton:
			item = self.itemAt(event.scenePos())
			if item:
				if item is self.__firstPoint:
					self.removeItem(item)
					self.__firstPoint = None
				elif item is self.__lastPoint:
					self.removeItem(item)
					self.__lastPoint = None
				self.update()

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
		if self.__firstPoint:
			self.removeItem(self.__firstPoint)
			self.__firstPoint = None
		if self.__lastPoint:
			self.removeItem(self.__lastPoint)
			self.__lastPoint = None
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
		return self.__firstPoint.pos(), self.__lastPoint.pos()