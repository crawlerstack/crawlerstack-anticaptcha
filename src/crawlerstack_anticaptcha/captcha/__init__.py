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
    if category == Captcha.Slider.value:
        image_captcha = SliderCaptcha(file)
        return image_captcha
    if category == Captcha.Numerical.value:
        num_captcha = NumericalCaptcha(file)
        return num_captcha
    return None
