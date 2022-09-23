"""Factory"""
from enum import EnumMeta

from crawlerstack_anticaptcha.utils import RotatedCategory, SliderCategory


class CaptchaFactory:
    """CaptchaFactory"""

    def __init__(self, category: str):
        self.category = category

    def create_captcha(self) -> EnumMeta | ModuleNotFoundError:
        """create_captcha"""
        if self.category == 'SliderCaptcha':
            return SliderCategory
        if self.category == 'RotatedCaptcha':
            return RotatedCategory
        raise ModuleNotFoundError
