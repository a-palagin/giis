__author__ = 'drain'


from PySide import QtCore, QtGui
from scene.Scene3D import Scene3D

class SceneView3D(QtGui.QGraphicsView):

    def __init__(self,parent = None):
        self.__scene = Scene3D()
        super(SceneView3D,self).__init__(self.__scene,parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)

