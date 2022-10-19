"""test numerical captcha"""

import pytest
from pytest_mock import MockerFixture

from crawlerstack_anticaptcha.captcha.numerical import NumCaptchaOcr
from crawlerstack_anticaptcha.captcha.numerical.captcha import NumCaptcha
from crawlerstack_anticaptcha.captcha.numerical.preprocessing import \
    Preprocessing
from crawlerstack_anticaptcha.captcha.numerical.train import NumericalModel


@pytest.mark.parametrize(
    'parsing_mode',
    [
        'model',
        'ocr'
    ]
)
def test_parse(parsing_mode, mocker, mock_path):
    """test parse"""
    save_single_image = mocker.patch.object(Preprocessing, 'save_single_image')
    if parsing_mode == 'ocr':
        mocker.patch.object(NumCaptcha, 'ocr_identification', return_value='1')
        identify = mocker.patch.object(NumericalModel, 'identify')
        with open(mock_path / 'foo.jpg', 'ab') as f:
            f.write(b'1')
        num_captcha = NumCaptcha(mock_path / 'foo.jpg')
        result = num_captcha.parse()
        save_single_image.assert_called()
        identify.assert_called()
        assert result == '1'
    else:
        with open(mock_path / 'foo.jpg', 'ab') as f:
            f.write(b'1')
        num_captcha = NumCaptcha(mock_path / 'foo.jpg')
        mocker.patch.object(NumericalModel, 'identify', return_value='1234')
        result = num_captcha.parse()
        save_single_image.assert_called()
        assert result == '1234'


@pytest.mark.parametrize(
    'code',
    [
        '123',
        '1234'
    ]
)
def test_check(mocker: MockerFixture, code):
    """test check"""
    num_captcha = NumCaptcha(mocker.MagicMock())
    if code == '123':
        assert not num_captcha.check(code)
    if code == '1234':
        assert num_captcha.check(code)


def test_ocr_identification(mocker: MockerFixture):
    """test_ocr_identification"""
    num_captcha = NumCaptcha(mocker.MagicMock())
    mocker.patch.object(NumCaptchaOcr, 'classification', return_value='1234.')
    result = num_captcha.ocr_identification(mocker.MagicMock())
    assert result == '1234'
