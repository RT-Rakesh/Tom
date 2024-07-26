from Logger.log_adapters import LogAdapter
class App_Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Create a new instance if one doesn't exist
        if cls._instance is None:
            cls._instance = super(App_Logger,cls).__new__(cls)
        else:
            print("Warning!!!! Loading the existing logger.")
        return cls._instance

    def __init__(self, adapter: LogAdapter):
        # if not hasattr(self, '_initialized'):
            self._initialized = True
            self._adapter = adapter
            self._log_levels = ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE']

    def log_message(self, level: str, message: str):
        level = level.upper()
        if level in self._log_levels:
            self._adapter.log(level, message)
        else:
            print(f"The level should be one of these {self._log_levels}.")
