"""Test cracker"""

import pytest

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha


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
    image_captcha = SliderCaptcha('image_file')
    if length == 0:
        image_captcha.canny_detection = mocker.MagicMock(return_value=length)
        assert 'failed' in image_captcha.parse()
    if length == 1:
        image_captcha.canny_detection = mocker.MagicMock(return_value=length)
        assert image_captcha.parse() == 1
