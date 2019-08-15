from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt import QGraphicsScene, QGraphicsView, QGraphicsItem

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

from tools.UI import UI

from data.Defaults import Defaults


class MatplotTinderUI(QWidget, UI):

    def __init__(self, parent=None):
        super().__init__(parent)

        matplot_widget = FigureCanvas(Figure())
        self._ax = matplot_widget.figure.subplots()

        self._scene = QGraphicsScene()
        self.matplot_graphics_widget = self._scene.addWidget(matplot_widget)
        self.matplot_graphics_widget.setFlag(QGraphicsItem.ItemIsMovable)
        self.matplot_graphics_widget.setRotation(45)

        self._view = QGraphicsView(self._scene)
        self._view.setGeometry(250, 250, 500, 500)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._view)
        self.setLayout(layout)

    def show_image(self, img, cmap=Defaults.cmap, interpolation='gaussian'):
        self._ax.clear()
        self._ax.axis('off')
        self._ax.imshow(img.data, cmap=cmap, interpolation=interpolation)
        self._ax.figure.canvas.draw()

    def connect_multi_classification_listener(self, action):
        pass

    def connect_single_classification_listener(self, action):
        pass

    def connect_skip_classification_listener(self, action):
        pass