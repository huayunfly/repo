import unittest
import os
from image.imageprocessing import ImageProcessor


class ImageResizeTestCase(unittest.TestCase):
    src = './~testsrc'
    dest = './~testdest'
    fmt = '.png'

    def setUp(self):
        if not os.path.isdir(ImageResizeTestCase.src):
            os.mkdir(ImageResizeTestCase.src)
        self._processor = ImageProcessor()
        self._processor.init_with_path(ImageResizeTestCase.src,
                                       ImageResizeTestCase.dest,
                                       ImageResizeTestCase.fmt, (200, 100))

    def test_resize(self):
        self._processor.size = (161, 100)
        self._processor.resize()

if __name__ == '__main__':
    unittest.main()
