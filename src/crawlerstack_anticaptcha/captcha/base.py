"""base captcha """
import logging
import os
from pathlib import Path

from crawlerstack_anticaptcha.config import settings


class BaseCaptcha:
    """BaseCaptcha"""
    image_split_path = Path(settings.CAPTCHA_IMAGE_PATH) / 'char'

    def __init__(self, background_image: Path, fore_image: Path = None, extra_content: str = None):
        self.background_image = background_image
        self.fore_image = fore_image
        self.extra_content = extra_content
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        if not self.image_split_path.exists():
            os.makedirs(self.image_split_path)

    def parse(self):
        """parse"""
        raise NotImplementedError
