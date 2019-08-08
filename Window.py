from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QColor
import h5py as h5
import numpy as np
import random


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self._main_widget = QWidget()
        self._image_label = QLabel()
        self._next_button = QPushButton('next')
        self._next_button.clicked.connect(self._show_random_image)
        layout = QVBoxLayout()
        layout.addWidget(self._image_label)
        layout.addWidget(self._next_button)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self._main_widget.setLayout(layout)
        self.setCentralWidget(self._main_widget)
        self.setGeometry(250, 250, 500, 500)
        self._load_data()
        self._show_random_image()

    def _load_data(self):
        with h5.File('images_to_classify_manually.h5', 'r') as file:
            self._data = np.array(file['X_test'])

    def _show_image(self, num):
        image = QImage(100, 100, QImage.Format_ARGB32)
        factor = 255 / self._data[num].max()

        for x in range(len(self._data[num])):
            for y in range(len(self._data[num][x])):
                color = QColor()
                color.setRed(int(self._data[num][x][y] * factor))
                color.setGreen(int(self._data[num][x][y] * factor))
                color.setBlue(int(self._data[num][x][y] * factor))
                color.setAlpha(255)
                image.setPixel(x, y, color.rgb())

        pixmap = QPixmap.fromImage(image)
        self._image_label.setPixmap(pixmap)
        self._image_label.setScaledContents(True)

    def _show_random_image(self):
        self._show_image(random.randint(0, 199))