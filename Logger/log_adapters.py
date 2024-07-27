from abc import ABC, abstractmethod


class LogAdapter(ABC):
    @abstractmethod
    def log(self, level, message):
        pass


class FileLogAdapter(LogAdapter):
    def __init__(self, filename):
        self._level = None
        self._message = None
        self._log_file_name = filename

    def log(self, level, message):
        with open(self._log_file_name, 'a') as f:
            f.write(f'{level}: {message}' + '\n')

class ConsoleLogAdapter(LogAdapter):
    def __init__(self):
        self._level = None
        self._message = None

    def log(self, level, message):
        print(f'{level}: {message}')