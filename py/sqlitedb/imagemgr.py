__author__ = 'yun_hua'

import sqlite3
import logging

class ImageMgr(object):
    """Manage images with words relationship in database,
       including create, read, update, delete.
    """
    def init_with_path(self, path):
        # assert(sqlite3_threadsafe)
        self._databasePath = path

    def __init__(self):
        self._databasePath = None
        self._conn = None

    @property
    def sqlpath(self):
        return self._databasePath

    @sqlpath.setter
    def sqlpath(self, value):
        if value is not None:
            self._databasePath = value

    @staticmethod
    def sqlite3_version():
        return sqlite3.sqlite_version

    def open(self):
        """Open database using path"""
        if self._conn is not None:
            return True
        self._conn = sqlite3.connect(self.sqlpath)
        if self._conn is not None:
            return True
        else:
            print "Opening database %r failed" % self._conn
            logging.debug("Opening database %r failed", self._conn)
            return False

    def close(self):
        """Close the database
        """
        if self._conn is None:
            return True

        self._conn.close()
        return True

    def create_db_table(self, sql):
        """sql e.g. "CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)"
        SQLite natively supports the following types: NULL, INTEGER, REAL, TEXT, BLOB.

        The following Python types can thus be sent to SQLite without any problem:
        Python type: SQLite type = {None: NULL, int: INTEGER, long: INTEGER, float: REAL,
        str(UTF8): TEXT, unicode: TEXT, buffer: BLOB}

        SQLite to Python:
        {NULL: None, INTEGER: int or long, REAL: float, TEXT: depends on text_factory,
        unicode by default, BLOB: buffer}
        """
        c = self._conn.cursor()
        res = c.execute(sql)
        if res is None:
            return False
        else:
            return True

    def insert_db_row(self, sql):
        """Insert a row in db"""
        c = self._conn.cursor()
        c.execute(sql)
        self._conn.commit()

    def query_db(self, query, params):
        """Query row, update db using sql.
        Using ? as a placeholder to construct a secure query instead of using Python string operation.
        e.g.
        t = ('RHAT',)
        c.execute('SELECT * FROM stocks WHERE symbol=?', t)

        NEVER DO THIS:
        symbol = 'RHAT'
        c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
        """
        c = self._conn.cursor()
        return c.execute(query, params)





