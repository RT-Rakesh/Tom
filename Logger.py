import datetime

class Logger:
    def __init__(self, log_file='TOM.log'):
        self.log_file = log_file

    def _write_log(self, level, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {level} - {message}"
        with open(self.log_file, 'a') as file:
            file.write(log_message + '\n')
        print(log_message)

    def log(self, level, message):
        self._write_log(level, message)

    def info(self, message):
        self.log('INFO', message)

    def warning(self, message):
        self.log('WARNING', message)

    def error(self, message):
        self.log('ERROR', message)

    def critical(self, message):
        self.log('CRITICAL', message)

    def debug(self, message):
        self.log('DEBUG', message)

    def exception(self, message):
        self.log('EXCEPTION', message)

    def fatal(self, message):
        self.log('FATAL', message)


logger = Logger()

logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
logger.debug("This is a debug message")
logger.exception("This is an exception message")
logger.fatal("This is a fatal message")
