"""numerical captcha"""
import logging
import re
from pathlib import Path

from crawlerstack_anticaptcha.captcha.numerical import NumCaptchaOcr
from crawlerstack_anticaptcha.captcha.numerical.preprocessing import \
    Preprocessing
from crawlerstack_anticaptcha.captcha.numerical.train import NumericalModel
from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.utils.exception import \
    NumericalCaptchaParseFailed


class NumCaptcha:
    """Numerical Captcha"""
    SLICE_DIR = Path(settings.IMAGE_SAVE_PATH) / 'numerical-captcha/char'

    def __init__(self, image_file: Path):
        self.image_file = image_file
        self.preprocess = Preprocessing(image_file)
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def parse(self):
        """parse"""
        self.preprocess.save_single_image()
        numerical_model = NumericalModel(self.SLICE_DIR)
        result = numerical_model.identify()
        if not self.check(result):
            with open(self.image_file, 'rb') as f:
                image = f.read()
            ocr_result = self.ocr_identification(image)
            if ocr_result:
                return ocr_result
            raise NumericalCaptchaParseFailed()
        return result

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
        ocr = NumCaptchaOcr()
        res = ocr.classification(image)
        res = ''.join(re.findall(r'\d+', res))
        return res
