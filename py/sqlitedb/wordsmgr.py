import sqlite3
import logging
from xml.dom.minidom import parse

__author__ = 'yun_hua'


class WordsMgr(object):
    """Manage images with words relationship in database,
       including create, read, update, delete.
    """
    def init_with_path(self, dbpath, xmlpath, imagedir):
        assert dbpath is not None, xmlpath is not None
        assert imagedir is not None
        if dbpath is None or xmlpath is None or imagedir is None:
            raise ValueError, "None parameters"
        self._databasePath = dbpath
        self._xmlPath = xmlpath
        self._imageDir = imagedir
        if self._dom is None:
            self._dom = parse(self.xmlpath)
            assert self._dom.documentElement.tagName == "words"

    def __init__(self):
        self._databasePath = None
        self._conn = None
        self._xmlPath = None
        self._dom = None
        self._sqladdtable = None
        self._sqladdrow = None
        self._imageDir = None

    @property
    def sqlpath(self):
        return self._databasePath

    @sqlpath.setter
    def sqlpath(self, value):
        if value is not None:
            self._databasePath = value

    @property
    def xmlpath(self):
        return self._xmlPath

    @xmlpath.setter
    def xmlpath(self, value):
        if value is not None:
            self._xmlPath = value

    @property
    def sqladdtable(self):
        return self._sqladdtable

    @sqladdtable.setter
    def sqladdtable(self, value):
        if value is not None:
            self._sqladdtable = value

    @property
    def sqladdrow(self):
        return self._sqladdrow

    @sqladdrow.setter
    def sqladdrow(self, value):
        if value is not None:
            self._sqladdrow = value

    def row_value(self):
        if self._dom is None:
            return None
        else:
            c = self._dom.childNodes[0].nextSibling

    @staticmethod
    def sqlite3_version():
        return sqlite3.sqlite_version

    def open(self):
        """Open database using path"""
        if self._conn is not None:
            return True
        try:
            self._conn = sqlite3.connect(self.sqlpath)
        except sqlite3.OperationalError, err:
            logging.debug(str(err))
            return False
        return True

    def close(self):
        """Close the database
        """
        if self._conn is None:
            return True

        self._conn.close()
        return True

    def create_db_table(self):
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
        if self._conn is None:
            return False
        try:
            c = self._conn.cursor()
            c.execute(self.sqladdtable)
        except sqlite3.OperationalError, err:
            logging.debug(str(err))
            return False
        return True

    def insert_db_rows(self, params):
        """Insert some rows in db"""
        c = self._conn.cursor()
        c.executemany(self.sqladdrow, params)
        self._conn.commit()

    def insert_db_row(self, param):
        """Insert a row in db"""
        c = self._conn.cursor()
        c.execute(self.sqladdrow, param)
        self._conn.commit()

    def word_row_params(self):
        """Build word database row params from xml in the fixed scheme"""
        elements = self._dom.documentElement.getElementsByTagName("item")
        params = []
        for element in elements:
            attrs = (element.getAttribute('word'),
                     element.getAttribute('us_phonetic'),
                     element.getAttribute('uk_phonetic'),
                     element.getAttribute('chs'),
                     element.getAttribute('chs_phonetic'),
                     int(element.getAttribute('category'))
                     )
            params.append(attrs)
        return params

    def image_row_params(self):
        """Generator for the image database row parameters"""
        elements = self._dom.documentElement.getElementsByTagName("item")
        for element in elements:
            attr = (element.getAttribute('word'),)
            path = self._imageDir + element.getAttribute('category') + '/' + element.getAttribute('word') + '.png'
            f = open(path, 'rb')
            try:
                b = buffer(f.read())
                yield (element.getAttribute('word'), b)
            finally:
                f.close()

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





