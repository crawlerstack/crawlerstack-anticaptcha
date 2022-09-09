"""Cracker"""
import logging

import cv2

from crawlerstack_anticaptcha.processing.preprocessing import \
    ImagePreprocessing


class SliderCaptchaServices:
    """SliderCaptchaServices"""

    def __init__(self, image_file: str):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.img_file = image_file

    def parse(self):
        """parse"""
        self.logger.info('Parse Captcha.')
        length = self.canny_detection()
        if length == 0:
            return 'Parsing failed, Please upload again.'
        return length

    def canny_detection(self):
        """canny_detection"""
        preprocessing = ImagePreprocessing(self.img_file)
        length = 0
        edge = cv2.Canny(preprocessing.morph_close(), 30, 80)
        counts, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for count in counts:
            x_coordinate, _y_coordinate, width, high = cv2.boundingRect(count)
            if x_coordinate < 50:
                continue
            if width < 60:
                continue
            if high < 60:
                continue
            length = x_coordinate
        return length
