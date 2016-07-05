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
        @param<size>: the processing image size in tuple (height, width)
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

    def resize(self):
        """Resize the image following 'crop' and 'size' steps"""
        if self._src is None or self._dest is None:
            return





