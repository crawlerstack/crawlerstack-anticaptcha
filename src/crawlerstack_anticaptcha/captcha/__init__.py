"""BaseCaptcha"""

from pathlib import Path

from crawlerstack_anticaptcha.captcha.numerical.captcha import NumericalCaptcha
from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha
from crawlerstack_anticaptcha.utils import SingletonMeta


class CaptchaParser(metaclass=SingletonMeta):
    """Captcha"""
    captcha_funcs = {
        'NumericalCaptcha': NumericalCaptcha,
        'SliderCaptcha': SliderCaptcha
    }

    def __init__(self, category: str):
        self.category = category

    def factory(self, background_image: Path, fore_image: Path, extra_content: str):
        """factory"""
        captcha_instance = self.captcha_funcs.get(self.category)(
            background_image=background_image,
            fore_image=fore_image,
            extra_content=extra_content
        )
        parse_result = captcha_instance.parse()
        return parse_result
