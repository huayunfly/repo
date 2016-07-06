from __future__ import division
from PIL import Image
import os


class ImageProcessor(object):
    """Image processing for the images, including crop, resize etcs"""

    def __init__(self):
        self._src = None
        self._dest = None
        self._format = None
        self._size = None

    def init_with_path(self, src, dest, fmt, size):
        """Initialzie with image lib parameters
        @param<src>: image library source path
        @param<dest>: processed image library path
        @param<fmt>: image format in '.png', '.bmp', etc. The suffix is used to create the image object path
        @param<size>: the processing image size in tuple (width, height)
        """
        if (src or dest or fmt or size) is None:
            raise ValueError('None value parameters')
        if not os.path.isdir(src):
            raise ValueError('src path is not valid')
        if not os.path.isdir(dest):
            os.mkdir(dest)
        self._src = src
        self._dest = dest
        self._format = fmt
        self._size = size

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError('value is invalid.')
        self._size = value

    def resize(self):
        """Batch resize the images in the source directory using the given size.
        The process keeps the scale (width / height) specified by size.
        """
        if self._src is None or self._dest is None:
            return
        for dirpath, dirname, filenames in os.walk(self._src):
            for name in filenames:
                if not name.endswith(self._format):
                    continue
                image = Image.open(os.path.join(dirpath, name))
                ratio = (image.size[0] / self._size[0]) / (image.size[1] / self._size[1])
                if ratio > 1.0:
                    x0 = int(image.size[0] * (1 - 1 / ratio) / 2)
                    y0 = 0
                    x1 = int(x0 + image.size[0] * (1 / ratio))
                    y1 = image.size[1]
                    cropped = image.crop((x0, y0, x1, y1))
                    scaled = cropped.resize(self._size)
                    scaled.save(os.path.join(self._dest, name))
                else:
                    x0 = 0
                    y0 = int(image.size[1] * (1 - 1 / ratio) / 2)
                    x1 = image.size[0]
                    y1 = int(y0 + image.size[1] * (1 / ratio))
                    cropped = image.crop((x0, y0, x1, y1))
                    scaled = cropped.resize(self._size)
                    scaled.save(os.path.join(self._dest, name))

    def crop(self):
        """Batch crop the images in the source directory using the given size"""
        if self._src is None or self._dest is None:
            return
        for dirpath, dirname, filenames in os.walk(self._src):
            for name in filenames:
                if not name.endswith(self._format):
                    continue
                image = Image.open(os.path.join(dirpath, name))
                if image.size[0] > self._size[0] and image.size[1] > self._size[1]:
                    x0 = (image.size[0] - self._size[0]) / 2
                    y0 = (image.size[1] - self._size[1]) / 2
                    x1 = x0 + self._size[0]
                    y1 = y0 + self._size[1]
                    cropped = image.crop((x0, y0, x1, y1))
                    cropped.save(os.path.join(self._dest, name))
