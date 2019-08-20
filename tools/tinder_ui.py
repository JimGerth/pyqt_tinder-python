import numpy as np
from PyQt5.Qt import QGestureRecognizer, QPointF, pyqtProperty
from PyQt5.QtCore import QEvent, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QImage
from PyQt5.QtWidgets import QWidget

from tools.ui import UI

from services.pan_gesture_recognizer import PanGestureRecognizer
from services.plot_service import PlotService

from materials.image import Image

from data.defaults import Defaults


class TinderUI(QWidget, UI):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._position = QPointF(0, 0)
        self._opacity = 1.0
        self._scale = 4.5
        self.setMinimumSize(600, 600)

        self._image = None
        self._show_title_card = True
        self._load_title_card()

        self.grabGesture(QGestureRecognizer.registerRecognizer(PanGestureRecognizer()))

    @pyqtProperty("QPointF")
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos
        self.update()

    @pyqtProperty("float")
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        self._opacity = opacity
        self.update()

    @pyqtProperty("float")
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self.update()

    @property
    def rotation(self):
        pic = [self.position.x(), -self.position.y()]
        pivot = [0, -self.height()]
        v1 = np.subtract(pic, pivot)
        v2 = np.subtract([0, 0], pivot)
        a = np.arccos(np.divide(np.abs(np.dot(v1, v2)), (np.linalg.norm(v1) * np.linalg.norm(v2))))
        if self.position.x() < 0:
            return -a * 10
        return a * 10

    def _load_title_card(self):
        title_card = QImage(Defaults.title_card_file_path)
        self.title_image = Image(None, None)
        self.title_image.q_image = title_card

    def event(self, event):
        if event.type() == QEvent.Gesture and event.gesture(Qt.PanGesture):
            self._pan_triggered(event.gesture(Qt.PanGesture))
        else:
            super().event(event)
        return True

    def wheelEvent(self, e):
        self.scale -= e.pixelDelta().y() * 0.01
        if self.scale < 0.1:
            self.scale = 0.1

    def paintEvent(self, event):
        painter = self._setup_painter()
        self._paint_circles(painter)
        self._paint_icons(painter)
        self._paint_image(painter)

    def _setup_painter(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Defaults.pen)
        return painter

    def _paint_circles(self, painter):
        painter.save()
        if self.position.x() > 0:
            painter.setBrush(Defaults.single_color)
            painter.drawEllipse(QPointF(self.width() / 2, 0),
                                (self.width() / 4) * (self.position.x() / (self.width() / 2)) / 2,
                                self.height() / 2 + self.height() * 0.1)
        else:
            painter.setBrush(Defaults.multi_color)
            painter.drawEllipse(QPointF(-self.width() / 2, 0),
                                (self.width() / 4) * (self.position.x() / (self.width() / 2)) / 2,
                                self.height() / 2 + self.height() * 0.1)
        if self.position.y() < 0:
            painter.setBrush(Defaults.skip_color)
            painter.drawEllipse(QPointF(0, -self.height() / 2), self.width() / 2 + self.width() * 0.1,
                                (self.height() / 4) * (-self.position.y() / (self.height() / 2)) / 2)
        else:
            painter.setBrush(Defaults.skip_color)
            painter.drawEllipse(QPointF(0, self.height() / 2), self.width() / 2 + self.width() * 0.1,
                                (self.height() / 4) * (-self.position.y() / (self.height() / 2)) / 2)
        painter.restore()

    def _paint_icons(self, painter):
        size = 60
        res = 256
        margin = 10
        opacity = 130/255 * (1 - np.linalg.norm([self.position.x(), self.position.y()]) / np.linalg.norm([self.width() / 2, self.height() / 2]))
        painter.setOpacity(opacity)

        painter.save()
        painter.translate(self.width() / 2 - size / 2 - margin, 0)
        if self.position.x() > 0:
            painter.translate(-self.position.x() * 0.1, 0)
            painter.setOpacity(opacity + 130/255 * self.position.x() / (self.width() / 2))
        painter.translate(-size / 2, -size / 2)
        painter.scale(size/res, size/res)
        painter.drawImage(0, 0, QImage(Defaults.check_icon_path))
        painter.restore()

        painter.save()
        painter.translate(-self.width() / 2 + size / 2 + margin, 0)
        if self.position.x() < 0:
            painter.translate(-self.position.x() * 0.1, 0)
            painter.setOpacity(opacity + 130 / 255 * -self.position.x() / (self.width() / 2))
        painter.translate(-size / 2, -size / 2)
        painter.scale(size / res, size / res)
        painter.drawImage(0, 0, QImage(Defaults.cross_icon_path))
        painter.restore()

        painter.save()
        painter.translate(0, -self.height() / 2 + size / 2 + margin)
        if self.position.y() < 0:
            painter.translate(0, -self.position.y() * 0.1)
            painter.setOpacity(opacity + 130 / 255 * -self.position.y() / (self.height() / 2))
        painter.translate(-size / 2, -size / 2)
        painter.scale(size / res, size / res)
        painter.drawImage(0, 0, QImage(Defaults.clock_icon_path))
        painter.restore()

        painter.save()
        painter.translate(0, self.height() / 2 - size / 2 - margin)
        if self.position.y() > 0:
            painter.translate(0, -self.position.y() * 0.1)
            painter.setOpacity(opacity + 130 / 255 * self.position.y() / (self.height() / 2))
        painter.translate(-size / 2, -size / 2)
        painter.scale(size / res, size / res)
        painter.drawImage(0, 0, QImage(Defaults.clock_icon_path))
        painter.restore()

    def _paint_image(self, painter):
        painter.save()
        iw = self._image.width or 250
        ih = self._image.height or 250

        # setting painter up to right location and orientation to draw
        painter.translate(self.position.x(), self.position.y())
        painter.rotate(self.rotation)
        painter.scale(self.scale, self.scale)
        painter.translate(-iw / 2, -ih / 2)
        painter.setOpacity(self.opacity)

        # drawing a shadow
        painter.setBrush(QColor(0, 0, 0, 10))
        painter.drawRect(2, 2, iw, ih)

        # drawing the image (or a rectangle if there is no image)
        if not self._image:
            painter.setBrush(QColor(150, 150, 150))
            painter.drawRect(0, 0, iw, ih)
        else:
            if self._show_title_card:
                painter.scale(100/1024, 100/1024)
                painter.drawImage(0, 0, self.title_image.q_image)
            else:
            #     painter.setCompositionMode(QPainter.CompositionMode_Source)
            #     painter.setBrush(QColor(0, 0, 0))
            #     painter.drawRoundedRect(0, 0, iw, ih, 2, 2)
            #     painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
                painter.drawImage(0, 0, self._image.q_image)
        painter.restore()

    def _reset(self, was_classified):
        if was_classified:
            self._show_title_card = False
            self.position = QPointF(0, 0)

            self.animation1 = QPropertyAnimation(self, b'opacity')
            self.animation1.setStartValue(0)
            self.animation1.setEndValue(1)
            self.animation1.setDuration(75)
            self.animation1.start()

            self.animation2 = QPropertyAnimation(self, b'scale')
            self.animation2.setStartValue(self.scale - 1)
            self.animation2.setEndValue(self.scale)
            self.animation2.setDuration(75)
            self.animation2.start()

        else:
            self.animation3 = QPropertyAnimation(self, b'position')
            self.animation3.setStartValue(self.position)
            self.animation3.setEndValue(QPointF(0, 0))
            self.animation3.setEasingCurve(QEasingCurve.OutBack)
            self.animation3.setDuration((np.linalg.norm([self.position.x(), self.position.y()]) / np.linalg.norm([self.width(), self.height()])) * 500)
            self.animation3.start()

    def _pan_triggered(self, pan_gesture):
        delta = pan_gesture.delta()
        self.position += delta * Defaults.sensibility
        if pan_gesture.state() == Qt.GestureFinished:
            self._reset(self._check_if_classified())

    def _check_if_classified(self):
        if self.position.x() > self.width() / 2 - self.width() * 0.1:
            if not self._show_title_card:
                self._classify_single()
            return True
        elif self.position.x() < -self.width() / 2 + self.width() * 0.1:
            if not self._show_title_card:
                self._classify_multi()
            return True
        elif self.position.y() < -self.height() / 2 + self.height() * 0.1 or self.position.y() > self.height() / 2 - self.height() * 0.1:
            if not self._show_title_card:
                self._classify_skip()
            return True
        return False

    def show_image(self, image, cmap=Defaults.cmap, interpolation='gaussian'):
        if not image.q_image:
            PlotService().convert_to_image(image)
        self._image = image
        self.update()

    def connect_single_classification_listener(self, action):
        self._classify_single = action

    def connect_skip_classification_listener(self, action):
        self._classify_skip = action

    def connect_multi_classification_listener(self, action):
        self._classify_multi = action
