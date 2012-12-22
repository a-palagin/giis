__author__ = 'drain'


import sys
from ui.Window import Window
from scene.Scene import  GraphicScene
from PySide import QtGui

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
    sys.exit()
