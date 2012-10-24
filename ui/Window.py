__author__ = 'drain'

from PySide import QtGui, QtCore

from ui.MenuBar import MenuBar
from ui.SceneView import SceneView

class Window(QtGui.QMainWindow):
	menuBarHeight = 20
	borderWidth = 3 #win 5
	borderHeight = 3
	def __init__(self):
		super(Window,self).__init__()
		self.__graphicsView = SceneView()
		self.__menuBar = MenuBar()
		self.setCentralWidget(self.__graphicsView)
		print self.__graphicsView.size()
		#self.setSizePolicy(QtCore.Qt.No)l
		#self.setFixedSize(self.__graphicsView.size() +\
		#                  QtCore.QSize(self.borderWidth,self.borderHeight + self.menuBarHeight))
		print self.size()
		self.setMenuBar(self.__menuBar)
