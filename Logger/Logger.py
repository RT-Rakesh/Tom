from Logger.log_adapters import LogAdapter
from Logger.log_observers import LogObserver
from typing import List
class App_Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Create a new instance if one doesn't exist
        if cls._instance is None:
            cls._instance = super(App_Logger,cls).__new__(cls)
        else:
            print("Warning!!!! Loading the existing logger.")
        return cls._instance

    def __init__(self):
        # if not hasattr(self, '_initialized'):
            self._initialized = True
            self._observers: List[LogObserver] = []
            self._log_levels = ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE']

    def add_observer(self, observer: LogObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: LogObserver):
        self._observers.remove(observer)

    def notify_observers(self, level: str, message: str):
        for observer in self._observers:
            observer.update(level, message)

    def log_message(self, level: str, message: str):
        level = level.upper()
        if level in self._log_levels:
            self.notify_observers(level, message)
        else:
            print(f"The level should be one of these {self._log_levels}.")
