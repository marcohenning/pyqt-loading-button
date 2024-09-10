import math
from qtpy.QtCore import QTimeLine, QEasingCurve, Qt
from qtpy.QtGui import QPainter, QPen, QColor
from qtpy.QtWidgets import QPushButton
from .worker import Worker
from .animation_type import AnimationType


class LoadingButton(QPushButton):

    def __init__(self, parent=None):
        super(LoadingButton, self).__init__(parent)

        self.__text = ''
        self.__action = None
        self.__running = False

        self.__animation_type = AnimationType.Circle
        self.__animation_speed = 1500
        self.__animation_width = 13
        self.__animation_thickness = 3
        self.__animation_color = QColor(0, 0, 0)

        self.__circle_speed_coefficient = 0.35
        self.__circle_span_speed = int(self.__animation_speed * self.__circle_speed_coefficient)
        self.__circle_minimum_span = 30
        self.__circle_maximum_span = 280
        self.__circle_span = self.__circle_maximum_span
        self.__circle_additional_rotation = 0
        self.__circle_previous_additional_rotation = 0

        self.__timeline_circle_rotation = QTimeLine(self.__animation_speed, self)
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

            if self.__animation_type == AnimationType.Circle:
                self.__timeline_circle_rotation.start()
                self.__timeline_circle_decrease_span.start()

            elif self.__animation_type == AnimationType.Dots:
                pass

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
        self.__circle_additional_rotation = self.__timeline_circle_increase_span.currentFrame() - self.__circle_minimum_span
        self.update()

    def __handle_timeline_circle_increase_span_start(self):
        self.__circle_previous_additional_rotation = (self.__circle_previous_additional_rotation + self.__circle_additional_rotation) % 360
        self.__timeline_circle_increase_span.start()

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.__running and self.__animation_type == AnimationType.Circle:

            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(self.__animation_color, self.__animation_thickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))

            x = math.floor((self.width() - self.__animation_width) / 2)
            y = math.ceil((self.height() - self.__animation_width) / 2)
            rotation = (self.__timeline_circle_rotation.currentFrame() - self.__circle_additional_rotation - self.__circle_previous_additional_rotation) % 360 * 16
            span = self.__circle_span * 16
            painter.drawArc(x, y, self.__animation_width, self.__animation_width, rotation, span)

        elif self.__running and self.__animation_type == AnimationType.Dots:
            pass

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
        if not self.__running:
            super().setText(self.__text)

    def setAction(self, action):
        self.__action = action
