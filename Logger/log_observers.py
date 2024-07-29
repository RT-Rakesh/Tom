from abc import ABC, abstractmethod

class LogObserver(ABC):
    @abstractmethod
    def update(self, level, message):
        pass

class ErrorLogObserver(LogObserver):
    def __init__(self, adapter):
        self.adapter = adapter

    def update(self, level, message):
        if level == 'ERROR':
            self.adapter.log(level, message)

class InfoLogObserver(LogObserver):
    def __init__(self, adapter):
        self.adapter = adapter

    def update(self, level, message):
        if level == 'INFO':
            self.adapter.log(level, message)