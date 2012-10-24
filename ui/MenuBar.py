__author__ = 'drain'

from PySide import QtGui, QtCore

from scene.SceneManager import SceneManger

class MenuBar(QtGui.QMenuBar):

	def __init__(self):
		super(MenuBar,self).__init__()
		self.__sceneManager = SceneManger()
		self.algorithmsMenu = self.addMenu("algorithms")
		self.settingsMenu = self.addMenu("settings")
		self.algorithmsMenu.addAction("DDA").triggered.connect(self.DDA)
		self.algorithmsMenu.addAction("Bresenham").triggered.connect(self.Bresenham)
		self.settingsMenu.addAction("set pixel size").triggered.connect(self.pixelSizeMenu)
		self.settingsMenu.addAction("clear").triggered.connect(self.clearScene)

	def DDA(self):
		self.__sceneManager.drawCDA()

	def pixelSizeMenu(self):
		newSize, ok = QtGui.QInputDialog.getInteger(self,"pixel size","pixel size:",
														self.__sceneManager.getPixelSize(),1,50,1)
		if ok:
			self.__sceneManager.setNewPixelSize(newSize)
		print "pixel size menu"

	def clearScene(self):
		self.__sceneManager.clearAll()
		print "clear scene"

	def Bresenham(self):
		self.__sceneManager.drawBresenham()


