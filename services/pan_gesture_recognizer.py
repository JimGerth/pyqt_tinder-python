from PyQt5.Qt import QGestureRecognizer
from PyQt5.Qt import QPointF
from PyQt5.Qt import QPanGesture
from PyQt5.QtCore import QEvent


class PanGestureRecognizer(QGestureRecognizer):

    def __init__(self):
        super().__init__()
        self.start_point = QPointF()
        self.panning = False

    def create(self, target):
        return QPanGesture()

    def recognize(self, gesture, watched, event):
        if event.type() == QEvent.MouseButtonPress:
            self.panning = True
            self.start_point = event.pos()
            gesture.setLastOffset(QPointF())
            gesture.setOffset(QPointF())
            return QGestureRecognizer.TriggerGesture

        if self.panning and event.type() == QEvent.MouseMove:
            gesture.setLastOffset(gesture.offset())
            gesture.setOffset(event.pos() - self.start_point)
            return QGestureRecognizer.TriggerGesture

        if event.type() == QEvent.MouseButtonRelease:
            end_point = event.pos()
            if self.start_point == end_point:
                self.panning = False
                return QGestureRecognizer.CancelGesture
            self.panning = False
            gesture.setLastOffset(gesture.offset())
            gesture.setOffset(end_point - self.start_point)
            return QGestureRecognizer.FinishGesture

        if event.type() == QEvent.MouseButtonDblClick:
            self.panning = False
            return QGestureRecognizer.FinishGesture

        if not event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseMove or event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseButtonDblClick:
            return QGestureRecognizer.Ignore