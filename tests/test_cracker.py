"""Test cracker"""
import os

import pytest

from crawlerstack_anticaptcha.services.cracker import SliderCaptchaServices


@pytest.mark.parametrize(
    'length',
    [
        0,
        1
    ]
)
def test_parse(mocker, length):
    """
    test_parse
    :param mocker:
    :param length:
    :return:
    """
    image_captcha = SliderCaptchaServices('image_file')
    if length == 0:
        image_captcha.canny_detection = mocker.MagicMock(return_value=length)
        assert 'failed' in image_captcha.parse()
    if length == 1:
        image_captcha.canny_detection = mocker.MagicMock(return_value=length)
        assert image_captcha.parse() == 1


def test_canny_detection():
    """test_canny_detection"""
    test_image_file = os.path.abspath('data/test.jpg')
    image_captcha = SliderCaptchaServices(test_image_file)
    assert image_captcha.canny_detection() == 106
