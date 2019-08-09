from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
import h5py as h5
import numpy as np
import random


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self._main_widget = QWidget()
        layout = QVBoxLayout()

        self._next_button = QPushButton('next')
        self._next_button.clicked.connect(self._show_random_image)

        self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.addToolBar(Qt.TopToolBarArea, NavigationToolbar(self._canvas, self))
        self._static_ax = self._canvas.figure.subplots()

        layout.addWidget(self._canvas)
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
        self._static_ax.clear()
        self._static_ax.imshow(self._data[num], cmap='Spectral_r', interpolation='gaussian')
        self._static_ax.figure.canvas.draw()

    def _show_random_image(self):
        self._show_image(random.randint(0, 199))