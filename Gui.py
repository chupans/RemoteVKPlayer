import sys
import music
from functools import partial

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class GuiController(QObject):
    """Proxy class that handles all interactions with the su.Puzzle class.

    This class does not have any UI elements. Instead it emits signals."""

    disc = pyqtSignal(str, arguments=['reason'])
    conn = pyqtSignal()
    newSong = pyqtSignal(int, str, arguments=['value', 'name'])
    pause = pyqtSignal()

    def __init__(self):
        super(GuiController, self).__init__()
        self.setup_mode = False
        self.mus = music.VKMusic(partial(self.conn.emit), partial(self.disc.emit), partial(self.newSong.emit), partial(self.pause.emit))

    def test(self):
        self.disc.emit('succ')

    @pyqtSlot()
    def abr(self):
        """Setup a random puzzle with a minimum number of assigned squares."""
        self.disc.emit('succ')

    @pyqtSlot(str, str)
    def connect(self, login, password):
        self.mus.connect(login, password)
        i = 2

    def stop(self):
        self.mus.stop_worker()


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    guiController = GuiController()
    ctx.setContextProperty('guiController', guiController)
    ctx.setContextProperty("RemoteMusicPlayerGUI", engine)

    qml = r'D:/work/RemoteMusicPlayer/Gui/main.qml'
    a = engine.load(qml)

    app.exec_()
    guiController.stop()

    sys.exit()
