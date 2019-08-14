import numpy as np
from PyQt5.Qt import QGestureRecognizer, QPointF, pyqtProperty
from PyQt5.QtCore import QEvent, Qt, QPropertyAnimation
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from tools.UI import UI

from services.PanGestureRecognizer import PanGestureRecognizer
from services.PlotService import PlotService


class TinderUI(QWidget, UI):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.position = QPointF(0, 0)
        self.scale_factor = 2
        self.current_step_scale_factor = 1
        self.setMinimumSize(100, 100)

        self._image = None

        id = QGestureRecognizer.registerRecognizer(PanGestureRecognizer())
        self.grabGesture(id)

    @property
    def rotation(self):
        pic = [self.position.x(), -self.position.y()]
        pivot = [0, -500]
        v1 = np.subtract(pic, pivot)
        v2 = np.subtract([0, 0], pivot)
        a = np.arccos(np.divide(np.abs(np.dot(v1, v2)), (np.linalg.norm(v1) * np.linalg.norm(v2))))
        if self.position.x() < 0:
            return -a * 10
        return a * 10

    def event(self, event):
        if event.type() == QEvent.Gesture and event.gesture(Qt.PanGesture):
            self.pan_triggered(event.gesture(Qt.PanGesture))
        else:
            super().event(event)
        return True

    def paintEvent(self, event):
        painter = QPainter(self)

        iw = self._image.width() or 250
        ih = self._image.height() or 250
        ww = self.width()
        wh = self.height()

        painter.translate(ww / 2, wh / 2)
        painter.translate(self.position.x(), self.position.y())
        painter.rotate(self.rotation)
        painter.scale(self.current_step_scale_factor * self.scale_factor, self.current_step_scale_factor * self.scale_factor)
        painter.translate(-iw / 2, -ih / 2)
        if not self._image:
            painter.drawRect(0, 0, iw, ih)
        else:
            painter.drawImage(0, 0, self._image)

    def mouseDoubleClickEvent(self, event):
        self._classify_skip()
        self.reset()

    def reset(self):
        #self.animation = QPropertyAnimation(self, b'position')
        #self.animation.setStartValue(self.position)
        #self.animation.setEndValue(QPointF(0, 0))
        #self.animation.setDuration(100)
        #self.animation.start()
        self.position = QPointF(0, 0)
        self.scale_factor = 2
        self.current_step_scale_factor = 1
        self.update()

    def pan_triggered(self, pan_gesture):
        delta = pan_gesture.delta()
        self.position += delta
        self.update()
        if pan_gesture.state() == Qt.GestureFinished:
            self.check_classification()
            self.reset()

    def check_classification(self):
        if self.position.x() > self.width() / 2:
            self._classify_single()
            self.reset()
        elif self.position.x() < -self.width() / 2:
            self._classify_multi()
            self.reset()
        elif self.position.y() < -self.height() / 2 or self.position.y() > self.height() / 2:
            self._classify_skip()
            self.reset()

    def resizeEvent(self, event):
        self.update()

    def show_image(self, image, cmap='Spectral_r', interpolation='gaussian'):
        self._image = PlotService().convert_to_image(image, cmap)
        self.update()

    def connect_single_classification_listener(self, action):
        self._classify_single = action

    def connect_skip_classification_listener(self, action):
        self._classify_skip = action

    def connect_multi_classification_listener(self, action):
        self._classify_multi = action
