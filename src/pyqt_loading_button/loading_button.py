from qtpy.QtWidgets import QPushButton
from .worker import Worker


class LoadingButton(QPushButton):

    def __init__(self, parent=None):
        super(LoadingButton, self).__init__(parent)

        self.__text = ''
        self.__action = None
        self.__running = False

        self.clicked.connect(self.__start_action)

    def __start_action(self):
        if self.__action and not self.__running:
            self.__running = True
            super().setText('')
            self.worker = Worker(self.__action)
            self.worker.finished.connect(self.__end_action)
            self.worker.start()

    def __end_action(self):
        super().setText(self.__text)
        self.__running = False

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
        if not self.__running:
            super().setText(self.__text)

    def setAction(self, action):
        self.__action = action
