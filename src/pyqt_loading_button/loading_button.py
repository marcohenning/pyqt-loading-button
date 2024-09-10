from qtpy.QtCore import QTimeLine, QEasingCurve, Qt
from qtpy.QtGui import QPainter, QPen, QColor
from qtpy.QtWidgets import QPushButton
from .worker import Worker


class LoadingButton(QPushButton):

    def __init__(self, parent=None):
        super(LoadingButton, self).__init__(parent)

        self.__text = ''
        self.__action = None
        self.__running = False

        self.__circle_rotation_speed = 2000
        self.__circle_span_speed = 700
        self.__circle_minimum_span = 30
        self.__circle_maximum_span = 280
        self.__circle_span = self.__circle_maximum_span
        self.__circle_additional_span = 0
        self.__circle_previous_additional_span = 0

        self.__timeline_circle_rotation = QTimeLine(self.__circle_rotation_speed, self)
        self.__timeline_circle_rotation.setFrameRange(360, 0)
        self.__timeline_circle_rotation.setLoopCount(0)
        self.__timeline_circle_rotation.setEasingCurve(QEasingCurve.Type.Linear)
        self.__timeline_circle_rotation.frameChanged.connect(self.update)

        self.__timeline_circle_decrease_span = QTimeLine(self.__circle_span_speed, self)
        self.__timeline_circle_decrease_span.setFrameRange(self.__circle_maximum_span, self.__circle_minimum_span)
        self.__timeline_circle_decrease_span.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.__timeline_circle_decrease_span.frameChanged.connect(self.__handle_timeline_circle_decrease_span)
        self.__timeline_circle_decrease_span.finished.connect(self.__handle_timeline_circle_increase_span_start)

        self.__timeline_circle_increase_span = QTimeLine(self.__circle_span_speed, self)
        self.__timeline_circle_increase_span.setFrameRange(self.__circle_minimum_span, self.__circle_maximum_span)
        self.__timeline_circle_increase_span.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.__timeline_circle_increase_span.frameChanged.connect(self.__handle_timeline_circle_increase_span)
        self.__timeline_circle_increase_span.finished.connect(self.__timeline_circle_decrease_span.start)

        self.clicked.connect(self.__start_action)

    def __start_action(self):
        if self.__action and not self.__running:
            self.__running = True
            super().setText('')
            self.worker = Worker(self.__action)
            self.worker.finished.connect(self.__end_action)
            self.worker.start()
            self.__timeline_circle_rotation.start()
            self.__timeline_circle_decrease_span.start()

    def __end_action(self):
        super().setText(self.__text)
        self.__timeline_circle_rotation.stop()
        self.__timeline_circle_decrease_span.stop()
        self.__timeline_circle_increase_span.stop()
        self.__running = False

    def __handle_timeline_circle_decrease_span(self):
        self.__circle_span = self.__timeline_circle_decrease_span.currentFrame()
        self.update()

    def __handle_timeline_circle_increase_span(self):
        self.__circle_span = self.__timeline_circle_increase_span.currentFrame()
        self.__circle_additional_span = self.__timeline_circle_increase_span.currentFrame() - self.__circle_minimum_span
        self.update()

    def __handle_timeline_circle_increase_span_start(self):
        self.__circle_previous_additional_span = (self.__circle_previous_additional_span + self.__circle_additional_span) % 360
        self.__timeline_circle_increase_span.start()

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.__running:

            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))

            rotation = (self.__timeline_circle_rotation.currentFrame() - self.__circle_additional_span - self.__circle_previous_additional_span) % 360 * 16
            span = self.__circle_span * 16
            painter.drawArc(10, 7, 15, 15, rotation, span)

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
        if not self.__running:
            super().setText(self.__text)

    def setAction(self, action):
        self.__action = action
