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
        _, _threshold = cv2.threshold(self.blur(), 100, 255, cv2.THRESH_BINARY)
        return _threshold

    def thresholding_black(self):
        """
        thresholding black
        :return:
        """
        _threshold = cv2.adaptiveThreshold(
            self.blur(), 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 23, 2
        )
        return _threshold

    def blur(self):
        """虚化模糊"""
        img = self.bg_image()
        img = cv2.bilateralFilter(img, 0, 50, 50)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        return img
