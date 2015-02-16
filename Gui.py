import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


#class Person(QObject):
#    def __init__(self, parent=None):
#        super(Person, self).__init__(parent)
#
#        # Initialise the value of the properties.
#        self._width = 48
#        self._height = 48
#        self._color = '#9c27b0'
#
#    @pyqtProperty('QString')
#    def color(self):
#        return self._color
#
#    @color.setter
#    def color(self, color):
#        self._color = color
#
#
#    @pyqtProperty(int)
#    def width(self):
#        return self._width
#
#    @width.setter
#    def width(self, width):
#        self._width = width
#
#
#    @pyqtProperty(int)
#    def height(self):
#        return self._height
#
#    @height.setter
#    def height(self, height):
#        self._height = height

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("RemoteMusicPlayerGUI", engine)

    qml = r'D:/work/RemoteMusicPlayer/Gui/main.qml'
    a = engine.load(qml)

    window = engine.rootObjects()[0]
    window.show()

    sys.exit(app.exec_())