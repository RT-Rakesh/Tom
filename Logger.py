from abc import ABC, abstractmethod

#singleton 
class singletone:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

# define chain of responsibility handler interface
class Logger(ABC):
    @abstractmethod
    def set_next(self, logger):
        pass

    @abstractmethod
    def log_message(self, level, message):
        #ex: level="error" , message="null pointer exception"
        pass


class BaseLogger(Logger):
    _next_logger = None  # link to the next handler/logger

    def set_next(self, logger):
        self._next_logger = logger
        return logger

    def log_message(self, level, message):
        if self._next_logger:
            return self._next_logger.log_message(level, message)
        return None


# define concrete handlers
class InfoLogger(BaseLogger):
    def log_message(self, level, message):
        print('-- In InfoLogger')
        if level == 'info':
            print(f'InfoLogger: {message}')
        else:
            super().log_message(level, message)

class WarningLogger(BaseLogger):
    def log_message(self, level, message):
        print('-- In WarningLogger')
        if level == 'warning':
            print(f'WarningLogger: {message}')
        else:
            super().log_message(level, message)

class ErrorLogger(BaseLogger):
    def log_message(self, level, message):
        print('-- In ErrorLogger')
        if level == 'error':
            print(f'ErrorLogger: {message}')
            print(f'ErrorLogger: sending alert via email to ...')
        else:
            super().log_message(level, message)

class CriticalLogger(BaseLogger):
    def log_message(self, level, message):
        print('-- In CriticalLogger')
        if level == 'critical':
            print(f'CriticalLogger: {message}')
        else:
            super().log_message(level, message)


