"""slider captcha"""

import cv2
import ddddocr

from crawlerstack_anticaptcha.captcha.base import BaseCaptcha
from crawlerstack_anticaptcha.captcha.slider.preprocessing import \
    ImagePreprocessing


class SliderCaptcha(BaseCaptcha):
    """SliderCaptchaChecker"""

    def parse(self) -> int:
        """parse"""
        if self.fore_image is None:
            length = self.canny_detection()
        else:
            length = self.ocr_parse()
        return int(length)

    def canny_detection(self):
        """canny detection"""
        preprocessing = ImagePreprocessing(bg_image_path=self.background_image)
        edge = cv2.Canny(preprocessing.blur(), 30, 80)
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
        preprocessing = ImagePreprocessing(bg_image_path=self.background_image)
        img = preprocessing.bg_image(gray=False).copy()
        length = 0
        counts, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        threshold_w = 4
        threshold_h = 2
        if img.shape[0] > 300 or img.shape[1] > 400:
            threshold_w = 8
            threshold_h = 4
        for count in counts:
            x_coordinate, _y_coordinate, width, high = cv2.boundingRect(count)
            if width < 45 or width > img.shape[1] / threshold_w:
                continue
            if high < 45 or high > img.shape[0] / threshold_h:
                continue
            if width / high > 1.3 or high / width > 1.3:
                continue
            if x_coordinate < 15 or len(count) < 45 or _y_coordinate < 1:
                continue
            length = x_coordinate
        self.logger.info('After parsing, the result is length=%s.', length)
        return length

    def ocr_parse(self):
        """use ocr parse captcha"""
        det = ddddocr.DdddOcr(show_ad=False, ocr=False)
        with open(self.background_image, 'rb') as f:
            bg_img = f.read()

        with open(self.fore_image, 'rb') as f:
            fore_img = f.read()
        res = det.slide_match(fore_img, bg_img, simple_target=True)
        return res.get('target')[0]
