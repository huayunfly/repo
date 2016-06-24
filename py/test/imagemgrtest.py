__author__ = 'yun_hua'

import unittest
import sqlite3
from sqlitedb.imagemgr import ImageMgr


class ImageMgrTestCase(unittest.TestCase):
    def setUp(self):
        self.mgr = ImageMgr()
        self.mgr.init_with_path(":memory")
        try:
            self.mgr.open()
        except sqlite3.OperationalError, err:
            print str(err)

    def tearDown(self):
        self.mgr.close()

    def test_db_open(self):
        self.assertTrue(self.mgr.open())

    def test_create_update(self):
        sql = """CREATE TABLE stocks
            (date text, trans text, symbol text, qty real, price real)"""
        self.assertTrue(self.mgr.create_db_table(sql))
        sql = """INSERT INTO stocks VALUES ('2016-06-22', "BUY", "RHAT", 100, 34.5) """
        self.mgr.insert_db_row(sql)
        queryError = """SELECT * FROM stocks WHERE symbolsss=?"""
        params = ("RHAT",)
        self.assertRaises(sqlite3.OperationalError, self.mgr.query_db(queryError, params))

        query = """SELECT * FROM stocks WHERE symbol=?"""
        for row in self.mgr.query_db(query, params):
            print row

if __name__ == '__main__':
    unittest.main()
