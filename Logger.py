class SingletonLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, output_type='console', log_file_name='log.txt', log_level='INFO'):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.output_type = output_type
            self.log_file_name = log_file_name
            self.log_level = log_level.upper()
            self.log_levels = ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE']
            self._next_logger = None

    def set_next(self, logger):
        self._next_logger = logger
        return logger

    def log_message(self, level, message):
        level = level.upper()
        if level == self.log_level:
            self._write_log(f'{level}: {message}')
        elif self._next_logger:
            return self._next_logger.log_message(level, message)
        return None

    def _write_log(self, message):
        if self.output_type == 'console':
            print(message)
        elif self.output_type == 'file':
            with open(self.log_file_name, 'a') as f:
                f.write(message + '\n')


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



trace_logger = Trace(output_type='file', log_file_name='app.log')
debug_logger = Debug(output_type='file', log_file_name='app.log')
critical_logger = Critical(output_type='file', log_file_name='app.log')
error_logger = Error(output_type='file', log_file_name='app.log')
warning_logger = Warning(output_type='file', log_file_name='app.log')
info_logger = Info(output_type='console')

info_logger.set_next(warning_logger).set_next(error_logger).set_next(critical_logger).set_next(debug_logger).set_next(trace_logger)
