__author__ = 'drain'

import math

from PySide import QtCore, QtGui

class Scene3D(QtGui.QGraphicsScene):

    vertexes = []
    faces =[]
    vertexes.append(QtGui.QVector4D(-100,-100,-100,1))
    vertexes.append(QtGui.QVector4D(-100,100,-100,1))
    vertexes.append(QtGui.QVector4D(100,100,-100,1))
    vertexes.append(QtGui.QVector4D(100,-100,-100,1))
    #############################################
    vertexes.append(QtGui.QVector4D(100,-100,100,1))
    vertexes.append(QtGui.QVector4D(100,100,100,1))
    vertexes.append(QtGui.QVector4D(-100,100,100,1))
    vertexes.append(QtGui.QVector4D(-100,-100,100,1))

    faces.append(((0,1),(1,2),(2,3),(3,0)))
    faces.append(((4,5),(5,6),(6,7),(7,4)))
    faces.append(((6,5),(5,2),(2,1),(1,6)))
    faces.append(((7,0),(0,3),(3,4),(4,7)))
    faces.append(((0,7),(7,6),(6,1),(1,0)))
    faces.append(((3,2),(2,5),(5,4),(4,3)))

    def __init__(self):
        super(Scene3D,self).__init__()
        self.transformMatrix = QtGui.QMatrix4x4(1, 0, 0, 0,
                                                0, 1, 0, 0,
                                                0, 0, 1, 0,
                                                0, 0, 0, 1)
        self.distance = 200.0
        self.lines = []
        self.timer =QtCore.QTimer()
        self.timer.timeout.connect(self.drawPolygons)
        self.timer.start(10)
        self.showHidden = True
        self.showProjection = False

    def rotateX(self,angle):
        c = math.cos(angle*math.pi/180)
        s = math.sin(angle*math.pi/180)
        matX = QtGui.QMatrix4x4(1, 0, 0, 0,
                                0, c, s, 0,
                                0,-s, c, 0,
                                0, 0, 0, 1)
        self.transformMatrix *= matX

    def rotateY(self,angle):
        c = math.cos(angle*math.pi/180)
        s = math.sin(angle*math.pi/180)
        matY = QtGui.QMatrix4x4(c, 0,-s, 0,
                                0, 1, 0, 0,
                                s, 0, c, 0,
                                0, 0, 0, 1)
        self.transformMatrix *= matY

    def rotateZ(self,angle):
        c = math.cos(angle*math.pi/180)
        s = math.sin(angle*math.pi/180)
        matZ = QtGui.QMatrix4x4(c, s, 0, 0,
                                -s, c, 0, 0,
                                0, 0, 1, 0,
                                0, 0, 0, 1)
        self.transformMatrix *= matZ

    def keyPressEvent(self,event, *args, **kwargs):
        if event.key() == QtCore.Qt.Key_Left:
            self.rotateX(-0.1 if event.modifiers() == QtCore.Qt.ControlModifier else 0.1)
        if event.key() == QtCore.Qt.Key_Right:
            self.rotateY(-0.1 if event.modifiers() == QtCore.Qt.ControlModifier else 0.1)
        if event.key() == QtCore.Qt.Key_Up:
            self.rotateZ(-0.1 if event.modifiers() == QtCore.Qt.ControlModifier else 0.1)
        if event.key() == QtCore.Qt.Key_Space:
            self.transformMatrix = QtGui.QMatrix4x4(1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1)
        if event.key() == QtCore.Qt.Key_H:
            self.showHidden = not self.showHidden
            print "hidden: %s" % self.showHidden
        if event.key() == QtCore.Qt.Key_P:
            self.showProjection = not self.showProjection
            print "projection: %s" % self.showProjection
        if event.key() == QtCore.Qt.Key_BracketRight:
            self.distance += 1.0
        if event.key() == QtCore.Qt.Key_BracketLeft:
            self.distance -= 1.0
        event.ignore()

    def drawPolygons(self):
        for i in xrange(len(self.vertexes)):
            self.vertexes[i] *= self.transformMatrix
        for line in self.lines:
            self.removeItem(line)
        self.lines = []
        for polygon in self.faces:
            self.drawPolygon(polygon)

    def checkVisiblePolygon(self,polygon,vertexes):
        P = QtGui.QVector3D(0,0,self.distance)
        p1 = vertexes[polygon[0][0]]
        p2 = vertexes[polygon[1][0]]
        p3 = vertexes[polygon[2][0]]
        vector1 = QtGui.QVector3D(p1.x()-p2.x(),p1.y()-p2.y(), p1.z()-p2.z())
        vector2 = QtGui.QVector3D(p3.x()-p2.x(),p3.y()-p2.y(), p3.z()-p2.z())
        a = vector1.y() * vector2.z() - vector2.y() * vector1.z()
        b = vector1.z() * vector2.x() - vector2.z() * vector1.x()
        c = vector1.x() * vector2.y() - vector2.x() * vector1.y()
        d = -1 * ( a * vector1.x() + b * vector1.y() + c * vector1.z() )
        val = (a * P.x() + b * P.y() + c*P.z() + d)
        return True if val > 0 else False

    def drawPolygon(self,polygon):
        vertexes = []
        if self.showProjection:
            vertexes = self.makeProjection()
        else:
            vertexes = self.vertexes
        if not self.showHidden:
            if self.checkVisiblePolygon(polygon,vertexes):
                for edge in polygon:
                    self.lines.append(self.addLine(vertexes[edge[0]].x(),vertexes[edge[0]].y(),
                                                   vertexes[edge[1]].x(),vertexes[edge[1]].y()))
        else:
            for edge in polygon:
                self.lines.append(self.addLine(vertexes[edge[0]].x(),vertexes[edge[0]].y(),
                                               vertexes[edge[1]].x(),vertexes[edge[1]].y()))

    def makeProjection(self):
        distanceMatrix = QtGui.QMatrix4x4(1, 0, 0, 0,
                                          0, 1, 0, 0,
                                          0, 0, 1, 1.0/self.distance,
                                          0, 0, 0, 1)
        vertexes = list(self.vertexes)
        for i in xrange(len(vertexes)):
            vertexes[i] *= distanceMatrix
            vertexes[i] /= vertexes[i].w()
        return vertexes