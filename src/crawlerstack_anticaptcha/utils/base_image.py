"""base_processing"""
import logging
from pathlib import Path

import cv2

from crawlerstack_anticaptcha.config import settings


class BasePreprocessing:
    """preprocessing"""
    captcha_image_path = Path(settings.CAPTCHA_IMAGE_PATH)

    def __init__(self, image: Path):
        self.img = str(image.resolve())
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @property
    def image(self):
        """
        对图像转灰度读取
        :return:
        """
        _img = cv2.imread(self.img, 0)
        return _img
