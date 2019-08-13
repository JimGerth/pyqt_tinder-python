import numpy as np
from PyQt5.Qt import QSwipeGesture, QPanGesture, QPinchGesture, QGestureRecognizer
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from tools.UI import UI

from services.PanGestureRecognizer import PanGestureRecognizer
from services.PlotService import PlotService


class TinderUI(QWidget, UI):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.position = 0
        self.horizontal_offset = 0
        self.vertical_offset = 0
        self.scale_factor = 1
        self.current_step_scale_factor = 1
        self.setMinimumSize(100, 100)

        self._image = None

        id = QGestureRecognizer.registerRecognizer(PanGestureRecognizer())
        self.grabGesture(id)

    def event(self, event):
        if event.type() == QEvent.Gesture: # gesture event
            self.gesture_event(event)
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
        painter.translate(self.horizontal_offset, self.vertical_offset)
        painter.rotate(self.get_rotation())
        painter.scale(self.current_step_scale_factor * self.scale_factor, self.current_step_scale_factor * self.scale_factor)
        painter.translate(-iw / 2, -ih / 2)
        if not self._image:
            painter.drawRect(0, 0, iw, ih)
        else:
            painter.drawImage(0, 0, self._image)

    def mouseDoubleClickEvent(self, event):
        self.reset()

    def reset(self):
        self.scale_factor = 1
        self.current_step_scale_factor = 1
        self.vertical_offset = 0
        self.horizontal_offset = 0
        self.update()

    def gesture_event(self, event):
        for gesture in event.gestures():
            if type(gesture) is QSwipeGesture:
                self.swipe_triggered(gesture)
            elif type(gesture) is QPanGesture:
                self.pan_triggered(gesture)
            if type(gesture) is QPinchGesture:
                self.pinch_triggered(gesture)

    def pan_triggered(self, pan_gesture):
        delta = pan_gesture.delta()
        self.horizontal_offset += delta.x()
        self.vertical_offset += delta.y()
        self.update()
        if pan_gesture.state() == Qt.GestureFinished:
            self.reset()

    def pinch_triggered(self, pinch_gesture):
        print('pinch triggered: {}'.format(pinch_gesture))

    def swipe_triggered(self, swipe_gesture):
        print('swipe triggered: {}'.format(swipe_gesture))

    def resizeEvent(self, event):
        self.update()

    def get_rotation(self):
        pic = [self.horizontal_offset, -self.vertical_offset]
        pivot = [0, -500]
        v1 = np.subtract(pic, pivot)
        v2 = np.subtract([0, 0], pivot)
        a = np.arccos(np.divide(np.abs(np.dot(v1, v2)), (np.linalg.norm(v1) * np.linalg.norm(v2))))
        if self.horizontal_offset < 0:
            return -a * 10
        return a * 10

    def show_image(self, image, cmap='Spectral_r', interpolation='gaussian'):
        self._image = PlotService().convert_to_image(image, cmap)
        self.update()

    def connect_single_classification_listener(self, action):
        pass

    def connect_skip_classification_listener(self, action):
        pass

    def connect_multi_classification_listener(self, action):
        pass
