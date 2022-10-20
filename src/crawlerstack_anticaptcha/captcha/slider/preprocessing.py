# -*- coding:utf-8 -*-
"""Preprocessing"""
import logging
from pathlib import Path

import cv2


class ImagePreprocessing:
    """ImagePreprocessing"""

    def __init__(self, img_file: Path):
        self.img_file = str(img_file.resolve())
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @property
    def image(self):
        """
        加载图片
        read_file
        :return:
        """
        img = cv2.imread(self.img_file, 0)
        return img

    def thresholding_white(self):
        """
        thresholding White
        :return:
        """
        _, _threshold = cv2.threshold(self.image, 200, 255, cv2.THRESH_BINARY)
        return _threshold

    def thresholding_black(self):
        """
        thresholding black
        :return:
        """
        _threshold = cv2.adaptiveThreshold(
            self.image, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 15, 2
        )
        return _threshold
