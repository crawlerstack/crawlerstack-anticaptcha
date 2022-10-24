"""Test cracker"""
import cv2
import pytest

from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha
from crawlerstack_anticaptcha.captcha.slider.preprocessing import \
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


@pytest.mark.parametrize(
    'length',
    [
        1,
        0,
        -1
    ]
)
def test_canny_detection(mocker, length):
    """test canny_detection"""
    image_captcha = SliderCaptcha(mocker.MagicMock())
    if length == 1:
        image_captcha.check = mocker.MagicMock(return_value=length)
        assert image_captcha.canny_detection() == 1
    if length == 0:
        mocker.patch.object(ImagePreprocessing, 'thresholding_black')
        mocker.patch.object(cv2, 'Canny')
        image_captcha.check = mocker.MagicMock(return_value=length)
        result = image_captcha.canny_detection()
        assert result == 0
    if length == -1:
        mocker.patch.object(cv2, 'Canny')
        image_captcha.check = mocker.MagicMock(return_value=length)
        result = image_captcha.canny_detection()
        assert result == 0


def test_check(mocker):
    """test check"""
