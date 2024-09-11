import sys
import time
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QApplication
from src.pyqt_loading_button import LoadingButton, AnimationType


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setWindowTitle('Example')
        self.setFixedSize(300, 165)

        # Button with circular animation
        self.button_1 = LoadingButton(self)
        self.button_1.setGeometry(94, 42, 110, 30)
        self.button_1.setText('Click me!')
        self.button_1.setAnimationType(AnimationType.Circle)  # Animation type
        self.button_1.setAnimationSpeed(2000)  # Time it takes until the animation is completed once (in ms)
        self.button_1.setAnimationColor(QColor(255, 255, 255))  # Animation color
        self.button_1.setAnimationWidth(15)  # Width of the entire animation
        self.button_1.setAnimationStrokeWidth(3)  # Width of the circle's brush stroke
        self.button_1.setAction(self.do_something)  # Connect the button to a method
        self.button_1.setStyleSheet(
            'color: white;'
            'background: #23395d;'
            'border: none;'
            'border-radius: 5px;'
        )

        # Button with dotted animation
        self.button_2 = LoadingButton(self)
        self.button_2.setGeometry(94, 82, 110, 30)
        self.button_2.setText('Click me!')
        self.button_2.setAnimationType(AnimationType.Dots) # Animation type
        self.button_2.setAnimationSpeed(800)  # Time it takes until the animation is completed once (in ms)
        self.button_2.setAnimationColor(QColor(255, 255, 255))  # Animation color
        self.button_2.setAnimationWidth(20)  # Width of the entire animation
        self.button_2.setAnimationStrokeWidth(4)  # Width of each dot
        self.button_2.setAction(self.do_something)  # Connect the button to a method
        self.button_2.setStyleSheet(
            'color: white;'
            'background: #23395d;'
            'border: none;'
            'border-radius: 5px;'
        )

    def do_something(self):
        time.sleep(5)  # Simulate long task


# Run the example
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
