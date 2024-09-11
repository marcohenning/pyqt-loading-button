# PyQt Loading Button

[![PyPI](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/pyqt-loading-button)
[![Python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/marcohenning/pyqt-loading-button)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/marcohenning/pyqt-loading-button/blob/master/LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-99%25-neon)](https://github.com/marcohenning/pyqt-loading-button)
[![Build](https://img.shields.io/badge/build-passing-neon)](https://github.com/marcohenning/pyqt-loading-button)

A QPushButton with built-in loading animations for PyQt and PySide.

![Main](https://github.com/user-attachments/assets/e4142cd2-9618-498e-a4c1-a2000239b0c9)

## About

The widget functions exactly like PyQt's regular `QPushButton` with the only exception being the way methods are connected to the `clicked` event. Normally you would connect a method to the `clicked` event by using the `connect()` method. On this button you use the `setAction()` method instead, passing a callable object as its parameter the same way you would do with the `connect()` method. The method will then get executed in a `QThread`, allowing the button to display a loading animation.

## Installation

```
pip install pyqt-loading-button
```

## Example

```python
import time
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow
from pyqt_loading_button import LoadingButton, AnimationType


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        # LoadingButton
        self.button_1 = LoadingButton(self)
        self.button_1.setText('Click me!')
        self.button_1.setAnimationType(AnimationType.Circle)
        self.button_1.setAnimationSpeed(2000)
        self.button_1.setAnimationColor(QColor(0, 0, 0))
        self.button_1.setAnimationWidth(15)
        self.button_1.setAnimationStrokeWidth(3)
        self.button_1.setAction(self.do_something)

    def do_something(self):
        time.sleep(5)  # Simulate long task
```

## Documentation

* **Setting the button text:**
```python
loading_button.setText('Click me!')
```

* **Setting the action connected to the clicked event:**
```python
def do_something():
    time.sleep(5)  # Simulate long task

loading_button.setAction(do_something)
```

* **Setting the animation type:**
```python
loading_button.setAnimationType(AnimationType.Circle)  # Circular animation
loading_button.setAnimationType(AnimationType.Dots)    # Dotted animation
```

* **Setting the animation speed:**
```python
# 2000 means each loop of the animation takes 2000 ms to complete
loading_button.setAnimationSpeed(2000)
```

* **Setting the animation width:**
```python
loading_button.setAnimationWidth(15)  # Total width of the animation is 15 px
```

* **Setting the animation stroke width:**
```python
loading_button.setAnimationStrokeWidth(3)  # Stroke width of the brush is 3 px
```

* **Setting the animation color:**
```python
loading_button.setAnimationColor(QColor(0, 0, 0))
```

* **Checking whether the action is currently being executed:**
```python
loading_button.isRunning()
```

**<br>All methods:**

| Method                                                  | Description                                                                              |
|---------------------------------------------------------|------------------------------------------------------------------------------------------|
| `text(self)`                                            | Get the current button text                                                              |
| `setText(self, text: str)`                              | Set the button text                                                                      |
| `setAction(self, action: callable)`                     | Set the action connected to the clicked event                                            |
| `isRunning(self)`                                       | Get whether the action is currently being executed                                       |
| `getAnimationType(self)`                                | Get the current animation type                                                           |
| `setAnimationType(self, animation_type: AnimationType)` | Set the animation type                                                                   |
| `getAnimationSpeed(self)`                               | Get the current animation speed (time it takes the animation to complete one loop in ms) |
| `setAnimationSpeed(self, speed: int)`                   | Set the animation speed (time it takes the animation to complete one loop in ms)         |
| `getAnimationWidth(self)`                               | Get the current width of the animation                                                   |
| `setAnimationWidth(self, width: int)`                   | Set the width of the animation                                                           |
| `getAnimationStrokeWidth(self)`                         | Get the current width of the brush stroke                                                |
| `setAnimationStrokeWidth(self, width: int)`             | Set the width of the brush stroke                                                        |
| `getAnimationColor(self)`                               | Get the current animation color                                                          |
| `setAnimationColor(self, color: QColor)`                | Set the animation color                                                                  |

## License

This software is licensed under the [MIT license](https://github.com/marcohenning/pyqt-loading-button/blob/master/LICENSE).
