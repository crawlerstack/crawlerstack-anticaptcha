"""Test cracker"""

from crawlerstack_anticaptcha.slider_captcha.captcha import SliderCaptcha
from crawlerstack_anticaptcha.slider_captcha.preprocessing import \
    ImagePreprocessing


def test_parse(mocker):
    """
    test_parse
    :param mocker:
    :return:
    """
    length = 1
    image_captcha = SliderCaptcha(mocker.MagicMock())
    image_captcha.canny_detection = mocker.MagicMock(return_value=length)
    assert image_captcha.parse() == 1


def test_canny_detection(mocker):
    """test canny_detection"""
    length = 1
    image_captcha = SliderCaptcha(mocker.MagicMock())
    ImagePreprocessing.thresholding_black = mocker.MagicMock()
    image_captcha.check = mocker.MagicMock(return_value=length)
    assert image_captcha.canny_detection() == 1
