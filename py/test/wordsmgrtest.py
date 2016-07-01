# _*_ coding: utf-8 _*_
__author__ = 'yun_hua'

import unittest
import sqlite3
from sqlitedb.wordsmgr import WordsMgr


class WordsMgrTestCase(unittest.TestCase):
    def setUp(self):
        self.mgr = WordsMgr()
        self.mgr.init_with_path(':memory:', '../res/words.xml', '../res/images/')
        try:
            self.mgr.open()
        except sqlite3.OperationalError, err:
            print str(err)

    def tearDown(self):
        self.mgr.close()

    def test_db_open(self):
        self.assertTrue(self.mgr.open())

    def test_create_words_db(self):
        """Test creating a workd database based on XML source file."""
        self.mgr.sqladdtable = 'CREATE TABLE english_lib \
            (word text, us_phonetic text, uk_phonetic text, chs text, chs_phonetic text, category integer)'
        self.assertTrue(self.mgr.create_db_table())

        self.mgr.sqladdrow = 'INSERT INTO english_lib VALUES (?, ?, ?, ?, ?, ?)'
        self.mgr.insert_db_rows(self.mgr.rowparams_word())
        # queryError = """SELECT * FROM english_lib WHERE symbolsss=?"""
        params = (u"star",)
        # self.assertRaises(sqlite3.OperationalError, self.mgr.query_db(queryError, params))

        query = 'SELECT * FROM english_lib WHERE word=?'
        for row in self.mgr.query_db(query, params):
            print row

    def test_create_image_db(self):
        self.mgr.sqladdtable = 'CREATE TABLE image_lib (word text, image blob)'
        self.assertTrue(self.mgr.create_db_table())


if __name__ == '__main__':
    unittest.main()
