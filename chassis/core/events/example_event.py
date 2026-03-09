from PySide6.QtCore import QObject, Signal

class ExampleEvent(QObject):
    start = Signal()
    end = Signal()
