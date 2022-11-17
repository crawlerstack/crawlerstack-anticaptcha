"""Test SliderCaptcha"""
from pathlib import Path

import ddddocr
import pytest

from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha


def test_image():
    """test image"""
    image_path = Path(r"C:\tmp\test\anticaptcha")
    for i in image_path.iterdir():
        slider = SliderCaptcha(background_image=i)
        print(i)
        print(slider.parse())


def test_ocr_parse(mocker, mock_path):
    """test ocr parse"""
    test_image_file = mock_path / 'foo.png'
    with open(test_image_file, 'wb') as f:
        f.write(b'1')
    slider_captcha = SliderCaptcha(background_image=test_image_file, fore_image=test_image_file)
    mocker.patch.object(ddddocr.DdddOcr, 'slide_match', return_value={'target': [1, 2]})
    res = slider_captcha.ocr_parse()
    assert res == 1


@pytest.mark.parametrize(
    'fore',
    [
        None, Path('foo')
    ]
)
def test_parse(mocker, fore):
    """test_parse"""
    if fore is None:
        slider_captcha = SliderCaptcha(background_image=mocker.MagicMock(), fore_image=fore)
        slider_captcha.canny_detection = mocker.MagicMock(return_value=1)
        assert slider_captcha.parse() == 1
    if fore:
        slider_captcha = SliderCaptcha(background_image=mocker.MagicMock(), fore_image=fore)
        slider_captcha.ocr_parse = mocker.MagicMock(return_value=1)
        assert slider_captcha.parse() == 1
