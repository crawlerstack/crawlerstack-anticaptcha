"""Preprocessing"""
import logging

from skimage import io
import cv2
import numpy as np


class ImagePreprocessing:
    """ImagePreprocessing"""

    def __init__(self, img_file: str):
        self.img_file = img_file
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @property
    def image(self):
        """read_file"""
        img = io.imread(self.img_file)
        return img

    @property
    def hsv(self):
        """gray"""
        hsv_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_img)  # pylint: disable=C0103,W0612
        return v

    def thresholding(self):
        """Thresholding"""
        _, thres = cv2.threshold(self.hsv, 190, 200, cv2.THRESH_BINARY_INV)
        return thres

    def morph_close(self):
        """morph_close"""
        _k = np.ones((3, 3), np.uint8)
        thres = cv2.morphologyEx(self.thresholding(), cv2.MORPH_CLOSE, _k)  # 闭运算
        return thres

    def show_img(self, image):
        """
        show image
        :param image:
        :return:
        """
        self.logger.info('Show image.')
        cv2.imshow('img', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
