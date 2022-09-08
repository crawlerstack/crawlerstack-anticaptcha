"""Cracker"""
import logging


class ImageTransformationServices:
    """ImageTransformationServices"""

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def parse(self):
        """parse"""
        self.logger.info('Parse Captcha.')
        return {'result': '10'}
