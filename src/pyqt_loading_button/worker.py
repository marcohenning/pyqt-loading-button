from qtpy.QtCore import QThread, Signal


class Worker(QThread):

    # Event
    finished = Signal()

    def __init__(self, action: callable):
        """Create a new Worker instance

        :param action: action to be executed
        """

        super(Worker, self).__init__()

        self.__action = action

    def run(self):
        """Executes the specified action"""

        self.__action()
        self.finished.emit()
