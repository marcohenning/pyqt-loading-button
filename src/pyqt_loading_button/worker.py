from qtpy.QtCore import QThread, Signal


class Worker(QThread):

    finished = Signal()

    def __init__(self, action):
        super(Worker, self).__init__()

        self.__action = action

    def run(self):
        self.__action()
        self.finished.emit()
