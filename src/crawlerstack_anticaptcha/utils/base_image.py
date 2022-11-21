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

    @staticmethod
    def image(image_path: Path, gray: bool):
        """image"""
        if gray:
            return cv2.imread(str(image_path), 0)
        return cv2.imread(str(image_path.resolve()))

    def fore_image(self, gray: bool = True) -> ndarray:
        """
        读取前景图
        :param gray:
        :return:
        """
        return self.image(self.bg_image_path, gray)

    def bg_image(self, gray: bool = True):
        """
        读取背景图
        :param gray:
        :return:
        """
        return self.image(self.fore_image_path, gray)
