"""numerical captcha"""
import re

import ddddocr

from crawlerstack_anticaptcha.captcha.base import BaseCaptcha
from crawlerstack_anticaptcha.captcha.numerical.model import NumericalModel
from crawlerstack_anticaptcha.captcha.numerical.preprocessing import \
    Preprocessing


class NumericalCaptcha(BaseCaptcha):
    """Numerical Captcha"""

    def parse(self):
        """parse"""
        preprocess = Preprocessing(self.background_image)
        preprocess.save_single_image()
        numerical_model = NumericalModel(self.image_split_path)
        result = numerical_model.identify()
        with open(self.background_image, 'rb') as f:
            image = f.read()
        ocr_result = self.ocr_identification(image)
        if result == ocr_result:
            return result
        self.logger.info('The ocr identification result is %s.', ocr_result)
        return ocr_result

    def check(self, code: str):
        """
        check
        :param code:
        :return:
        """
        if len(code) < 4:
            self.logger.debug('Abnormal image segmentation, use ocr identification.')
            return False
        return True

    def ocr_identification(self, image):
        """
        ocr identification
        :param image:
        :return:
        """
        self.logger.debug('Use OCR identification.')
        ocr = ddddocr.DdddOcr(show_ad=False)
        res = ocr.classification(image)
        res = ''.join(re.findall(r'\d+', res))
        return res
