from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from tools.UI import UI


class MainToolUI(QWidget, UI):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_views()
        self._setup_layouts()

    def _setup_views(self):
        self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self._static_ax = self._canvas.figure.subplots()
        self.window().addToolBar(Qt.TopToolBarArea, NavigationToolbar(self._canvas, self))

        self._single_button = QPushButton('single')
        self._single_button.setStyleSheet('background-color: #68c160')
        self._skip_button = QPushButton('skip')
        self._skip_button.setStyleSheet('background-color: #6895c1')
        self._multi_button = QPushButton('multi')
        self._multi_button.setStyleSheet('background-color: #ce423e')

    def _setup_layouts(self):
        button_layout = QHBoxLayout()
        button_layout.addWidget(self._single_button)
        button_layout.addWidget(self._skip_button)
        button_layout.addWidget(self._multi_button)
        button_layout.setSpacing(5)
        # button_layout.setContentsMargins(0, 7, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(self._canvas)
        layout.addLayout(button_layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def show_image(self, img, cmap='Spectral_r', interpolation='gaussian'):
        self._static_ax.clear()
        self._static_ax.axis('off')
        self._static_ax.imshow(img.data, cmap=cmap, interpolation=interpolation)
        self._static_ax.figure.canvas.draw()

    def connect_single_classification_listener(self, action):
        self._single_button.clicked.connect(action)

    def connect_skip_classification_listener(self, action):
        self._skip_button.clicked.connect(action)

    def connect_multi_classification_listener(self, action):
        self._multi_button.clicked.connect(action)
