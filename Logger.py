#!/usr/bin/python

import os

from RuntimeGlobalSettings import RuntimeGlobalSettings as settings

class Logger():
    def __init__(self, log_files=[], disabled_output_console=None, disabled_output_files=None):
        self.settings = settings.getInstance()
        _settings = self.settings

        self.log_files = log_files
        self.disabled_output_console = _settings.disabled_output_console if disabled_output_console is None else disabled_output_console
        self.disabled_output_files = _settings.disabled_output_files if disabled_output_files is None else disabled_output_files

    # ------- Private methods

    # private method, must be called in standart scenario from function 'logWithTimestamp'
    def log(self, msg, end=None):
        if self.disabled_output_console != True:
            print(msg, end=(end if end is not None else '\n'))

        if self.disabled_output_files != True:
            if not os.path.exists('output'):
                os.mkdir('output')
            if not os.path.exists('output/logs'):
                os.mkdir('output/logs')
            for log_file in self.log_files:
                with open(f'output/logs/log_{log_file}.txt', 'a') as log_file:
                    log_file.write(msg + (end if end is not None else '\n'))

    # private method, must be called in standart scenario from functions:
    # - 'logInfo'
    # - 'logDebug'
    # - 'logError'
    def logWithTimestamp(self, prefix, msg, end=None):
        from datetime import datetime

        now = datetime.now()
        timestamp = now.strftime('%d/%m/%Y %H:%M:%S')

        new_msg = f'{prefix} [{timestamp}] {msg}'
        self.log(new_msg, end)

    # ------- Public methods

    def logInfo(self, msg='', end=None):
        self.logWithTimestamp('[INFO]', msg, end)

    def logDebug(self, msg='', end=None):
        self.logWithTimestamp('[DEBUG]', msg, end)

    def logError(self, msg='', end=None):
        self.logWithTimestamp('[ERROR]', msg, end)
