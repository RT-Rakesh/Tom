
import unittest
import os
from Logger.log_adapters import FileLogAdapter, ConsoleLogAdapter
from Logger.log_observers import ErrorLogObserver, InfoLogObserver
from Logger.Logger  import App_Logger


class TestAppLogger(unittest.TestCase):

    def setUp(self):
        self.logger = App_Logger()
        self.logger._observers = []  # Clear any existing observers for isolation

    def tearDown(self):
        App_Logger._instance = None  # Reset the singleton instance for isolation in tests

    def test_singleton_behavior(self):
        logger2 = App_Logger()
        self.assertIs(self.logger, logger2)

    def test_add_remove_observer(self):
        file_adapter = FileLogAdapter('test_log.txt')
        error_observer = ErrorLogObserver(file_adapter)
        info_observer = InfoLogObserver(file_adapter)
        self.logger.add_observer(error_observer)
        self.logger.add_observer(info_observer)
        self.assertIn(error_observer, self.logger._observers)
        self.assertIn(info_observer, self.logger._observers)

        self.logger.remove_observer(error_observer)
        self.logger.remove_observer(info_observer)
        self.assertNotIn(error_observer, self.logger._observers)
        self.assertNotIn(info_observer, self.logger._observers)

    def test_error_log_observer(self):
        filename = 'test_log.txt'
        file_adapter = FileLogAdapter(filename)
        error_observer = ErrorLogObserver(file_adapter)
        self.logger.add_observer(error_observer)
        self.logger.log_message('info', 'File info message')  # This should not be logged
        self.logger.log_message('error', 'File error message')

        with open(filename, 'r') as f:
            logs = f.readlines()

        self.assertNotIn('INFO: File info message\n', logs)
        self.assertIn('ERROR: File error message\n', logs)

        os.remove(filename)  # Clean up

    def test_info_log_observer(self):
        filename = 'test_log.txt'
        file_adapter = FileLogAdapter(filename)
        info_observer = InfoLogObserver(file_adapter)
        self.logger.add_observer(info_observer)
        self.logger.log_message('info', 'File info message')
        self.logger.log_message('error', 'File error message')  # This should not be logged

        with open(filename, 'r') as f:
            logs = f.readlines()

        self.assertIn('INFO: File info message\n', logs)
        self.assertNotIn('ERROR: File error message\n', logs)

        os.remove(filename)  # Clean up

if __name__ == '__main__':
    unittest.main()