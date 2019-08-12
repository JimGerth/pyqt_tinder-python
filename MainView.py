from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MainView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self._static_ax = self._canvas.figure.subplots()
        self.window().addToolBar(Qt.TopToolBarArea, NavigationToolbar(self._canvas, self))

        self._next_button = QPushButton('next')

        layout = QVBoxLayout()
        layout.addWidget(self._canvas)
        layout.addWidget(self._next_button)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def _show_image(self, img, cmap='Spectral_r', interpolation='gaussian'):
        self._static_ax.clear()
        self._static_ax.axis('off')
        self._static_ax.imshow(img, cmap=cmap, interpolation=interpolation)
        self._static_ax.figure.canvas.draw()
