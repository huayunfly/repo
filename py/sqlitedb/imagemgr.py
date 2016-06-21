__author__ = 'yun_hua'

import sqlite3

class ImageMgr(object):
    """Manage images with words relationship in database,
       including create, read, update, delete.
    """
    def init_with_path(self, path):
        # assert(sqlite3_threadsafe)
        self.__databasePath = path

    def __init__(self):
        self.__databasePath = None
        self.__db = None

    def get_sqlite_path(self):
        if self.__databasePath is None:
            return ":memory:"
        else:
            return self.__databasePath

    sqlitePath = property(get_sqlite_path)

    def open(self):
        conn = sqlite3.connect(self.sqlitePath)
        if conn in not None:
            return True
        else:
            return False


