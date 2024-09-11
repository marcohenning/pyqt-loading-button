import time
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor, QPaintEvent
from PyQt6.QtTest import QTest
from pytestqt.qt_compat import qt_api
from src.pyqt_loading_button.loading_button import LoadingButton, AnimationType


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    assert loading_button.text() == ''
    assert not loading_button.isRunning()
    assert loading_button.getAnimationType() == AnimationType.Circle
    assert loading_button.getAnimationSpeed() == 2000
    assert loading_button.getAnimationWidth() == 15
    assert loading_button.getAnimationStrokeWidth() == 3
    assert loading_button.getAnimationColor() == QColor(0, 0, 0)


def test_set_text(qtbot):
    """Test setting the button text"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    loading_button.setText('Test')
    assert loading_button.text() == 'Test'


def test_set_animation_type(qtbot):
    """Test setting the animation type"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    loading_button.setAnimationType(AnimationType.Dots)
    assert loading_button.getAnimationType() == AnimationType.Dots


def test_set_animation_speed(qtbot):
    """Test setting the animation speed"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    loading_button.setAnimationSpeed(1000)
    assert loading_button.getAnimationSpeed() == 1000


def test_set_animation_width(qtbot):
    """Test setting the animation width"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    loading_button.setAnimationWidth(20)
    assert loading_button.getAnimationWidth() == 20


def test_set_animation_stroke_width(qtbot):
    """Test setting the animation stroke width"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    loading_button.setAnimationStrokeWidth(5)
    assert loading_button.getAnimationStrokeWidth() == 5


def test_set_animation_color(qtbot):
    """Test setting the animation color"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    color = QColor(255, 0, 0)
    loading_button.setAnimationColor(color)
    assert loading_button.getAnimationColor() == color


def test_click_event_circle(qtbot):
    """Test the click event for the circular animation"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    def action():
        time.sleep(2)

    loading_button.setAction(action)
    loading_button.setAnimationType(AnimationType.Circle)
    loading_button.setAnimationSpeed(1000)

    assert not loading_button.isRunning()

    loading_button.clicked.emit()

    paint_event = QPaintEvent(QRect(0, 0, 0, 0))
    qt_api.QtWidgets.QApplication.instance().postEvent(loading_button, paint_event)
    assert loading_button.isRunning()

    QTest.qWait(2250)
    assert not loading_button.isRunning()


def test_click_event_dots(qtbot):
    """Test the click event for the dotted animation"""

    loading_button = LoadingButton()
    qtbot.addWidget(loading_button)

    def action():
        time.sleep(2)

    loading_button.setAction(action)
    loading_button.setAnimationType(AnimationType.Dots)
    loading_button.setAnimationSpeed(1000)

    assert not loading_button.isRunning()

    loading_button.clicked.emit()

    paint_event = QPaintEvent(QRect(0, 0, 0, 0))
    qt_api.QtWidgets.QApplication.instance().postEvent(loading_button, paint_event)
    assert loading_button.isRunning()

    QTest.qWait(2250)
    assert not loading_button.isRunning()
