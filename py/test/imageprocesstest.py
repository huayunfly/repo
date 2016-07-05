import unittest
from image.imageprocessing import ImageProcessor


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._processor = ImageProcessor()
        self._processor.init_with_path('./testsrc', './testdest', '.png', ())

    def test_resize(self):
        self._processor.resize()

if __name__ == '__main__':
    unittest.main()
