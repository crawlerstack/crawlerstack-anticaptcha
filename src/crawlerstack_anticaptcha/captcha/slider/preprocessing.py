# -*- coding:utf-8 -*-
"""Preprocessing"""

import cv2

from crawlerstack_anticaptcha.utils.base_image import BasePreprocessing


class ImagePreprocessing(BasePreprocessing):
    """ImagePreprocessing"""

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
