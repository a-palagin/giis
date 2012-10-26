__author__ = 'drain'


import thread
from PySide import QtGui, QtCore

from scene.SceneManager import SceneManger

class MenuBar(QtGui.QMenuBar):

	def __init__(self):
		super(MenuBar,self).__init__()
		self.__sceneManager = SceneManger()
		self.lineMenu = self.addMenu("Line")
		self.curveMenu = self.addMenu("Curve")
		self.settingsMenu = self.addMenu("settings")
		self.lineMenu.addAction("DDA").triggered.connect(self.DDA)
		self.lineMenu.addAction("Bresenham").triggered.connect(self.Bresenham)
		self.curveMenu.addAction("Bresenham").triggered.connect(self.test)
		self.settingsMenu.addAction("set pixel size").triggered.connect(self.pixelSizeMenu)
		self.settingsMenu.addAction("clear").triggered.connect(self.clearScene)
		debugMode = self.settingsMenu.addAction("debug mode")
		debugMode.setCheckable(True)
		debugMode.triggered.connect(self.debugTrigger)

	def pixelSizeMenu(self):
		newSize, ok = QtGui.QInputDialog.getInteger(self,"pixel size","pixel size:",
														self.__sceneManager.getPixelSize(),2,50,1)
		if ok:
			self.__sceneManager.setNewPixelSize(newSize)
		print "pixel size menu"

	def clearScene(self):
		self.__sceneManager.clearAll()
		print "clear scene"

	def debugTrigger(self):
		self.__sceneManager.setDebugMode(not self.__sceneManager.isDebugMode())


	def Bresenham(self):
		self.__sceneManager.drawBresenham()

	def DDA(self):
		self.__sceneManager.drawDDA()


	def test(self):
		self.__sceneManager.drawCurve()