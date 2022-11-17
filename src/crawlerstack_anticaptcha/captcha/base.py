"""base captcha """
import logging
from pathlib import Path


class BaseCaptcha:
    """BaseCaptcha"""

    def __init__(self, background_image: Path, fore_image: Path = None, extra_content: str = None):
        self.background_image = background_image
        self.fore_image = fore_image
        self.extra_content = extra_content
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def parse(self):
        """parse"""
        raise NotImplementedError
