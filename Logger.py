#!/usr/bin/python

class Logger():
    __instance = None

    @staticmethod
    def getLogger(verbose):
        """Static access method."""
        if Logger.__instance == None:
            return Logger(verbose)
        return Logger.__instance

    def __init__(self, verbose):
        """Virtually private constructor."""
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self
            Logger.__instance.verbose = verbose

    def log(self, msg, end=None):
        if self.verbose:
            print(msg, end=(end if end is not None else '\n'))
        else:
            print('Not verbose:', msg, end=(end if end is not None else '\n'))

