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

        # Animation settings
        self.__animation_type = AnimationType.Circle
        self.__animation_speed = 2000
        self.__animation_width = 15
        self.__animation_stroke_width = 3
        self.__animation_color = QColor(0, 0, 0)

        # Animation settings (Circle)
        self.__circle_speed_coefficient = 0.35
        self.__circle_span_speed = int(self.__animation_speed * self.__circle_speed_coefficient)
        self.__circle_minimum_span = 30
        self.__circle_maximum_span = 280
        self.__circle_span = self.__circle_maximum_span
        self.__circle_additional_rotation = 0
        self.__circle_previous_additional_rotation = 0

        # Animation settings (Dots)
        self.__dots_speed_coefficient = 0.3
        self.__dots_single_speed = int(self.__animation_speed * self.__dots_speed_coefficient)
        self.__dots_easing_curve = QEasingCurve.Type.InOutSine
        self.__dots_offset_1 = 0
        self.__dots_offset_2 = 0
        self.__dots_offset_3 = 0

        # Animation timelines (Circle)
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

        # Animation timelines (Dots)
        self.__timeline_dots_up_1 = QTimeLine(self.__dots_single_speed, self)
        self.__timeline_dots_up_1.setFrameRange(0, self.__animation_stroke_width)
        self.__timeline_dots_up_1.setEasingCurve(self.__dots_easing_curve)
        self.__timeline_dots_up_1.frameChanged.connect(self.__handle_timeline_dots_up_1)

        self.__timeline_dots_down_1 = QTimeLine(self.__dots_single_speed, self)
        self.__timeline_dots_down_1.setFrameRange(self.__animation_stroke_width, 0)
        self.__timeline_dots_down_1.setEasingCurve(self.__dots_easing_curve)
        self.__timeline_dots_down_1.frameChanged.connect(self.__handle_timeline_dots_down_1)
        self.__timeline_dots_up_1.finished.connect(self.__timeline_dots_down_1.start)

        self.__timeline_dots_up_2 = QTimeLine(self.__dots_single_speed, self)
        self.__timeline_dots_up_2.setFrameRange(0, self.__animation_stroke_width)
        self.__timeline_dots_up_2.setEasingCurve(self.__dots_easing_curve)
        self.__timeline_dots_up_2.frameChanged.connect(self.__handle_timeline_dots_up_2)

        self.__timeline_dots_down_2 = QTimeLine(self.__dots_single_speed, self)
        self.__timeline_dots_down_2.setFrameRange(self.__animation_stroke_width, 0)
        self.__timeline_dots_down_2.setEasingCurve(self.__dots_easing_curve)
        self.__timeline_dots_down_2.frameChanged.connect(self.__handle_timeline_dots_down_2)
        self.__timeline_dots_up_2.finished.connect(self.__timeline_dots_down_2.start)

        self.__timeline_dots_up_3 = QTimeLine(self.__dots_single_speed, self)
        self.__timeline_dots_up_3.setFrameRange(0, self.__animation_stroke_width)
        self.__timeline_dots_up_3.setEasingCurve(self.__dots_easing_curve)
        self.__timeline_dots_up_3.frameChanged.connect(self.__handle_timeline_dots_up_3)

        self.__timeline_dots_down_3 = QTimeLine(self.__dots_single_speed, self)
        self.__timeline_dots_down_3.setFrameRange(self.__animation_stroke_width, 0)
        self.__timeline_dots_down_3.setEasingCurve(self.__dots_easing_curve)
        self.__timeline_dots_down_3.frameChanged.connect(self.__handle_timeline_dots_down_3)
        self.__timeline_dots_down_3.finished.connect(self.__timeline_dots_up_1.start)
        self.__timeline_dots_up_3.finished.connect(self.__timeline_dots_down_3.start)

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
            self.__timeline_dots_up_1.start()
            self.update()

    def __end_action(self):
        super().setText(self.__text)

        self.__timeline_circle_rotation.stop()
        self.__timeline_circle_decrease_span.stop()
        self.__timeline_circle_increase_span.stop()

        self.__timeline_dots_up_1.stop()
        self.__timeline_dots_down_1.stop()
        self.__timeline_dots_up_2.stop()
        self.__timeline_dots_down_2.stop()
        self.__timeline_dots_up_3.stop()
        self.__timeline_dots_down_3.stop()

        self.__running = False
        self.update()

    def __handle_timeline_circle_decrease_span(self):
        self.__circle_span = self.__timeline_circle_decrease_span.currentFrame()
        self.update()

    def __handle_timeline_circle_increase_span(self):
        self.__circle_span = self.__timeline_circle_increase_span.currentFrame()
        self.__circle_additional_rotation = self.__timeline_circle_increase_span.currentFrame() - self.__circle_minimum_span
        self.update()

    def __handle_timeline_circle_increase_span_start(self):
        self.__circle_previous_additional_rotation = (self.__circle_previous_additional_rotation +
                                                      self.__circle_additional_rotation) % 360
        self.__timeline_circle_increase_span.start()

    def __handle_timeline_dots_up_1(self, value):
        self.__dots_offset_1 = self.__timeline_dots_up_1.currentFrame()
        if value > 0.75 and self.__timeline_dots_up_2.state() == QTimeLine.State.NotRunning:
            self.__timeline_dots_up_2.start()
        self.update()

    def __handle_timeline_dots_down_1(self):
        self.__dots_offset_1 = self.__timeline_dots_down_1.currentFrame()
        self.update()

    def __handle_timeline_dots_up_2(self, value):
        self.__dots_offset_2 = self.__timeline_dots_up_2.currentFrame()
        if value > 0.75 and self.__timeline_dots_up_3.state() == QTimeLine.State.NotRunning:
            self.__timeline_dots_up_3.start()
        self.update()

    def __handle_timeline_dots_down_2(self):
        self.__dots_offset_2 = self.__timeline_dots_down_2.currentFrame()
        self.update()

    def __handle_timeline_dots_up_3(self):
        self.__dots_offset_3 = self.__timeline_dots_up_3.currentFrame()
        self.update()

    def __handle_timeline_dots_down_3(self):
        self.__dots_offset_3 = self.__timeline_dots_down_3.currentFrame()
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.__running and self.__animation_type == AnimationType.Circle:

            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(self.__animation_color, self.__animation_stroke_width,
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))

            diameter = self.__animation_width - self.__animation_stroke_width
            x = math.floor((self.width() - diameter) / 2)
            y = math.ceil((self.height() - diameter) / 2)
            rotation = (self.__timeline_circle_rotation.currentFrame() -
                        self.__circle_additional_rotation -
                        self.__circle_previous_additional_rotation) % 360 * 16
            span = self.__circle_span * 16

            painter.drawArc(x, y, diameter, diameter, rotation, span)

        elif self.__running and self.__animation_type == AnimationType.Dots:

            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(self.__animation_color)

            true_width = math.ceil(self.__animation_width / 3) * 2 + self.__animation_stroke_width
            x_dot_1 = math.ceil((self.width() - true_width) / 2)
            x_dot_2 = x_dot_1 + math.ceil(self.__animation_width / 3)
            x_dot_3 = x_dot_2 + math.ceil(self.__animation_width / 3)
            y = math.ceil((self.height() - self.__animation_stroke_width) / 2)

            painter.drawEllipse(x_dot_1, y - self.__dots_offset_1,
                                self.__animation_stroke_width, self.__animation_stroke_width)
            painter.drawEllipse(x_dot_2, y - self.__dots_offset_2,
                                self.__animation_stroke_width, self.__animation_stroke_width)
            painter.drawEllipse(x_dot_3, y - self.__dots_offset_3,
                                self.__animation_stroke_width, self.__animation_stroke_width)

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
        if not self.__running:
            super().setText(self.__text)

    def setAction(self, action: callable):
        self.__action = action

    def isRunning(self) -> bool:
        return self.__running

    def getAnimationType(self) -> AnimationType:
        return self.__animation_type

    def setAnimationType(self, animation_type: AnimationType):
        self.__animation_type = animation_type

    def getAnimationSpeed(self) -> int:
        return self.__animation_speed

    def setAnimationSpeed(self, speed: int):
        self.__animation_speed = speed

        self.__circle_span_speed = int(self.__animation_speed * self.__circle_speed_coefficient)
        self.__dots_single_speed = int(self.__animation_speed * self.__dots_speed_coefficient)

        self.__timeline_circle_rotation.setDuration(self.__animation_speed)
        self.__timeline_circle_decrease_span.setDuration(self.__circle_span_speed)
        self.__timeline_circle_increase_span.setDuration(self.__circle_span_speed)

        self.__timeline_dots_up_1.setDuration(self.__dots_single_speed)
        self.__timeline_dots_down_1.setDuration(self.__dots_single_speed)
        self.__timeline_dots_up_2.setDuration(self.__dots_single_speed)
        self.__timeline_dots_down_2.setDuration(self.__dots_single_speed)
        self.__timeline_dots_up_3.setDuration(self.__dots_single_speed)
        self.__timeline_dots_down_3.setDuration(self.__dots_single_speed)

    def getAnimationWidth(self) -> int:
        return self.__animation_width

    def setAnimationWidth(self, width: int):
        self.__animation_width = width

    def getAnimationStrokeWidth(self) -> int:
        return self.__animation_stroke_width

    def setAnimationStrokeWidth(self, width: int):
        self.__animation_stroke_width = width

    def getAnimationColor(self) -> QColor:
        return self.__animation_color

    def setAnimationColor(self, color: QColor):
        self.__animation_color = color
