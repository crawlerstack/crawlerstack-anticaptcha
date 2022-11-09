"""numerical captcha"""
import logging
import os
import re
from pathlib import Path

import ddddocr

from crawlerstack_anticaptcha.captcha.numerical.model import NumericalModel
from crawlerstack_anticaptcha.captcha.numerical.preprocessing import \
    Preprocessing
from crawlerstack_anticaptcha.config import settings


class NumericalCaptcha:
    """Numerical Captcha"""
    image_split_path = Path(settings.CAPTCHA_IMAGE_PATH) / 'numerical-captcha/char'

    def __init__(self, image_file: Path):
        self.image_file = image_file
        self.preprocess = Preprocessing(image_file)
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        if not self.image_split_path.exists():
            os.makedirs(self.image_split_path)

    def parse(self):
        """parse"""
        self.preprocess.save_single_image()
        numerical_model = NumericalModel(self.image_split_path)
        result = numerical_model.identify()
        with open(self.image_file, 'rb') as f:
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
