__author__ = 'drain'

from PySide import QtGui, QtCore

from ui.MenuBar import MenuBar
from ui.SceneView import SceneView
from ui.SceneView3D import SceneView3D

class Window(QtGui.QMainWindow):
    menuBarHeight = 20
    borderWidth = 3 #win 5
    borderHeight = 3
    _3D = "3d"
    _2D = "2d"
    def __init__(self):
        super(Window,self).__init__()
        self.__currentMode = self._2D
        self.__graphicsView2D = SceneView(self)
        self.__graphicsView3D = SceneView3D(self)
        self.__centralWidget = QtGui.QStackedWidget()
        self.__centralWidget.addWidget(self.__graphicsView2D)
        self.__centralWidget.addWidget(self.__graphicsView3D)
        self.__centralWidget.setCurrentWidget(self.__graphicsView2D)
        self.__menuBar = MenuBar()
        self.setCentralWidget(self.__centralWidget)
        self.setMenuBar(self.__menuBar)

    def keyPressEvent(self,event , *args, **kwargs):
        if event.key() == QtCore.Qt.Key_1:
            if not self.__currentMode == self._2D:
                self.__currentMode = self._2D
                self.__centralWidget.setCurrentWidget(self.__graphicsView2D)
                print "2d"
        elif event.key() == QtCore.Qt.Key_2:
            if not self.__currentMode == self._3D:
                self.__currentMode = self._3D
                self.__centralWidget.setCurrentWidget(self.__graphicsView3D)
                print "3d"

