from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt import QGraphicsScene, QGraphicsView, QGestureRecognizer, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QEvent, QPropertyAnimation

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

import numpy as np

from tools.UI import UI

from services.PanGestureRecognizer import PanGestureRecognizer

from data.Defaults import Defaults


class MatplotTinderUI(QWidget, UI):

    def __init__(self, parent=None):
        super().__init__(parent)

        matplot_widget = FigureCanvas(Figure())
        self._ax = matplot_widget.figure.subplots()

        self._scene = QGraphicsScene()
        self.matplot_graphics_widget = self._scene.addWidget(matplot_widget)
        self.matplot_graphics_widget.setParent(self)


        self.red_brush = QBrush(Qt.SolidPattern)
        self.red_brush.setColor(QColor(255, 0, 0, 50))

        self.pen = QPen()
        self.pen.setColor(QColor(0, 0, 0, 0))


        self._scene.addEllipse(0, self.height()/2, self.height()/2, self.height(), QPen(Qt.NoPen), self.red_brush)




        self._view = QGraphicsView(self._scene)
        self._view.setGeometry(250, 250, 500, 500)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._view)
        self.setLayout(layout)

        id = QGestureRecognizer.registerRecognizer(PanGestureRecognizer())
        self.grabGesture(id)

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
        self.skip = action

    def event(self, event):
        if event.type() == QEvent.Gesture and event.gesture(Qt.PanGesture):
            self.pan_triggered(event.gesture(Qt.PanGesture))
        else:
            super().event(event)
        return True

    def pan_triggered(self, pan_gesture):
        delta = pan_gesture.delta()
        self.matplot_graphics_widget.setPos(self.matplot_graphics_widget.x() + delta.x(), self.matplot_graphics_widget.y() + delta.y())
        if pan_gesture.state() == Qt.GestureFinished:
            # self._check_if_classified()
            self.reset()

    def mouseDoubleClickEvent(self, a0):
        # self.reset()
        print('mouseclick')
        self.skip()

    def reset(self):
        self.animation = QPropertyAnimation(self.matplot_graphics_widget, b'pos')
        self.animation.setStartValue(self.matplot_graphics_widget.pos())
        self.animation.setEndValue(QPointF(100, 100))
        self.animation.setDuration(100)
        self.animation.start()

    def paintEvent(self, event):
        self.matplot_graphics_widget.setRotation(self.get_rotation())
        self.update()

    def get_rotation(self):
        pic = [self.matplot_graphics_widget.x(), -self.matplot_graphics_widget.y()]
        pivot = [0, -500]
        v1 = np.subtract(pic, pivot)
        v2 = np.subtract([0, 0], pivot)
        a = np.arccos(np.divide(np.abs(np.dot(v1, v2)), (np.linalg.norm(v1) * np.linalg.norm(v2))))
        if self.matplot_graphics_widget.x() < 0:
            return -a * 10
        return a * 10