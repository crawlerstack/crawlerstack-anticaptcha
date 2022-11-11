"""BaseCaptcha"""

from pathlib import Path

from crawlerstack_anticaptcha.captcha.numerical.captcha import NumericalCaptcha
from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha
from crawlerstack_anticaptcha.utils import SingletonMeta


class CaptchaParser(metaclass=SingletonMeta):
    """Captcha"""
    captcha_funcs = {'NumericalCaptcha': NumericalCaptcha}

    def __init__(self, category: str, background_image: Path, fore_image: Path = None, extra_content: str = None):
        self.category = category
        self.background_image = background_image
        self.fore_image = fore_image
        self.extra_content = extra_content

    def factory(self):
        """factory"""
        captcha_instance = self.captcha_funcs.get(self.category)(
            background_image=self.background_image,
            fore_image=self.fore_image,
            extra_content=self.extra_content
        )
        parse_result = captcha_instance.parse()
        return parse_result
