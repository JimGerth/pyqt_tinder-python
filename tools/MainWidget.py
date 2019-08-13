from PyQt5.QtCore import QDir
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow

from tools.ImageWidget import ImageWidget


class MainWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setCentralWidget(ImageWidget(self))
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        geometry = QRect(0, 0, screen_geometry.width() * 3 / 4, screen_geometry.height() * 3 / 4)
        geometry.moveCenter(screen_geometry.center())
        self.setGeometry(geometry)

    def open_directory(self, path):
        self.setWindowTitle(QDir.toNativeSeparators(path))
        self.centralWidget().open_directory()

    def grab_gestures(self, gestures):
        self.centralWidget().grab_gestures(gestures)