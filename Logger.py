class SingletonLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Create a new instance if one doesn't exist
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, output_type='console', log_file_name='log.txt', log_level='INFO'):
        # Initialize only if the instance is not already initialized
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.output_type = output_type
            self.log_file_name = log_file_name
            self.log_level = log_level.upper()
            self.log_levels = ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE']
            self._next_logger = None  # Next logger in the chain of responsibility

    def set_next(self, logger):
        # Set the next logger in the chain
        self._next_logger = logger
        return logger

    def log_message(self, level, message):
        # Log the message if the level matches, otherwise pass it to the next logger
        level = level.upper()
        if level == self.log_level:
            self._write_log(f'{level}: {message}')
        elif self._next_logger:
            return self._next_logger.log_message(level, message)
        return None

    def _write_log(self, message):
        # Write the log message to the console or a file
        if self.output_type == 'console':
            print(message)
        elif self.output_type == 'file':
            with open(self.log_file_name, 'a') as f:
                f.write(message + '\n')


# Concrete loggers with specific log levels
class Info(SingletonLogger):
    def __init__(self, output_type='console', log_file_name='log.txt'):
        super().__init__(output_type, log_file_name, 'INFO')

class Warning(SingletonLogger):
    def __init__(self, output_type='console', log_file_name='log.txt'):
        super().__init__(output_type, log_file_name, 'WARN')

class Error(SingletonLogger):
    def __init__(self, output_type='console', log_file_name='log.txt'):
        super().__init__(output_type, log_file_name, 'ERROR')

class Critical(SingletonLogger):
    def __init__(self, output_type='console', log_file_name='log.txt'):
        super().__init__(output_type, log_file_name, 'FATAL')

class Debug(SingletonLogger):
    def __init__(self, output_type='console', log_file_name='log.txt'):
        super().__init__(output_type, log_file_name, 'DEBUG')

class Trace(SingletonLogger):
    def __init__(self, output_type='console', log_file_name='log.txt'):
        super().__init__(output_type, log_file_name, 'TRACE')

# Initialize loggers and set up the chain of responsibility
trace_logger = Trace(output_type='file', log_file_name='app.log')
debug_logger = Debug(output_type='file', log_file_name='app.log')
critical_logger = Critical(output_type='file', log_file_name='app.log')
error_logger = Error(output_type='file', log_file_name='app.log')
warning_logger = Warning(output_type='file', log_file_name='app.log')
info_logger = Info(output_type='console')

# Link the loggers in a chain
info_logger.set_next(warning_logger).set_next(error_logger).set_next(critical_logger).set_next(debug_logger).set_next(trace_logger)
