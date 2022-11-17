# -*- coding : utf-8-*-
"""base_processing"""

import logging
from pathlib import Path

import cv2
from numpy import ndarray

from crawlerstack_anticaptcha.config import settings


def show_img(image):
    """
    show image
    :param image:
    :return:
    """
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class BasePreprocessing:
    """preprocessing"""
    captcha_image_path = Path(settings.CAPTCHA_IMAGE_PATH)

    def __init__(self, bg_image_path: Path, fore_image_path: Path = None):
        self.bg_image_path = bg_image_path
        self.fore_image_path = fore_image_path
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def fore_image(self, gray: bool = True) -> ndarray:
        """
        读取前景图
        :param gray:
        :return:
        """
        if gray:
            return cv2.imread(str(self.fore_image_path.resolve()), 0)
        return cv2.imread(str(self.fore_image_path.resolve()))

    def bg_image(self, gray: bool = True):
        """
        读取背景图
        :param gray:
        :return:
        """
        if gray:
            return cv2.imread(str(self.bg_image_path.resolve()), 0)
        return cv2.imread(str(self.bg_image_path.resolve()))
