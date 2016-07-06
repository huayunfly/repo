import unittest
from image.imageprocessing import ImageProcessor


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._processor = ImageProcessor()
        self._processor.init_with_path('./testsrc', './testdest', '.png', (200, 100))

    def test_resize(self):
        self._processor.size = (161, 100)
        self._processor.resize()

if __name__ == '__main__':
    unittest.main()
