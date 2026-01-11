from PySide6.QtCore import QObject
from .example_event import ExampleEvent

class EventBus(QObject):
    def __init__(self):
        super().__init__()
        self._events = {}
        self._register_events()
    
    def _register_events(self):
        # 注册所有事件类
        self._events['example'] = ExampleEvent()
    
    def get_event(self, event_name):
        return self._events.get(event_name)
    
    # 快捷方法
    @property
    def example(self):
        return self.get_event('example')

# 实例化全局事件总线
event_bus = EventBus()
