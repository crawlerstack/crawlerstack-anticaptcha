"""BaseCaptcha"""

from pathlib import Path

from crawlerstack_anticaptcha.captcha.numerical.captcha import NumericalCaptcha
from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha
from crawlerstack_anticaptcha.utils.schema import Captcha


def captcha_factory(category: str, file: Path):
    """
    captcha
    :param file:
    :param category:
    :return:
    """
    captcha_instance = None
    if category == Captcha.Numerical.value:
        captcha_instance = NumericalCaptcha(file)
    return captcha_instance.parse()
