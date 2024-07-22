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

    def log_message(self, level, message):
        # Log the message if the level matches
        level = level.upper()
        if level == self.log_level:
            self._write_log(f'{level}: {message}')

    def _write_log(self, message):
        # Write the log message to the console or a file
        if self.output_type == 'console':
            print(message)
        elif self.output_type == 'file':
            with open(self.log_file_name, 'a') as f:
                f.write(message + '\n')

