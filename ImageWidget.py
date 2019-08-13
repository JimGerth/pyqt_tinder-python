from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPainter
from PyQt5.Qt import QSwipeGesture, QPanGesture, QPinchGesture
from PanGestureRecognizer import PanGestureRecognizer
from PyQt5.Qt import QGestureRecognizer


class ImageWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.position = 0
        self.horizontal_offset = 0
        self.vertical_offset = 0
        self.rotation_angle = 0
        self.scale_factor = 1
        self.current_step_scale_factor = 1
        self.setMinimumSize(100, 100)

        self.current_image = None

        id = QGestureRecognizer.registerRecognizer(PanGestureRecognizer())
        self.grabGesture(id)

    def grab_gestures(self, gestures):
        for gesture in gestures:
            self.grabGesture(gesture)

    def event(self, event):
        if event.type() == QEvent.Gesture: # gesture event
            self.gesture_event(event)
        else:
            super().event(event)
        return True

    def paintEvent(self, event):
        painter = QPainter(self)

        iw = 50 # self.current_image.width()
        ih = 100 # self.current_image.height()
        ww = self.width()
        wh = self.height()

        painter.translate(ww / 2, wh / 2)
        painter.translate(self.horizontal_offset, self.vertical_offset)
        painter.rotate(self.rotation_angle)
        painter.scale(self.current_step_scale_factor * self.scale_factor, self.current_step_scale_factor * self.scale_factor)
        painter.translate(-iw / 2, -ih / 2)
        # painter.drawImage(0, 0, self.current_image)
        painter.drawRect(0, 0, iw, ih)

    def mouseDoubleClickEvent(self, event):
        self.rotation_angle = 0
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

    def pinch_triggered(self, pinch_gesture):
        print('pinch triggered: {}'.format(pinch_gesture))

    def swipe_triggered(self, swipe_gesture):
        print('swipe triggered: {}'.format(swipe_gesture))

    def resizeEvent(self, event):
        self.update()

