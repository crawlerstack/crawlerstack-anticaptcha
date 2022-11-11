"""slider captcha"""

import cv2

from crawlerstack_anticaptcha.captcha.base import BaseCaptcha
from crawlerstack_anticaptcha.captcha.slider.preprocessing import \
    ImagePreprocessing


class SliderCaptcha(BaseCaptcha):
    """SliderCaptchaChecker"""

    def parse(self):
        """parse"""
        self.logger.info('Parse Captcha.')
        length = self.canny_detection()
        return length

    def canny_detection(self):
        """canny detection"""
        preprocessing = ImagePreprocessing(self.image)
        edge = cv2.Canny(preprocessing.thresholding_white(), 30, 80)
        length = self.check(edge)
        if length > 0:
            return length
        if length == 0:
            edge = cv2.Canny(preprocessing.thresholding_black(), 30, 80)
            length = self.check(edge)
            return length
        return length == 0

    def check(self, edge):
        """
        check
        :param edge:
        :return:
        """
        length = 0
        counts, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for count in counts:
            x_coordinate, _y_coordinate, width, high = cv2.boundingRect(count)
            if width < 45 or width > 65:
                continue
            if high < 45:
                continue
            if len(count) < 45:
                continue
            length = x_coordinate
        self.logger.info('After parsing, the result is length=%s.', length)
        return length
