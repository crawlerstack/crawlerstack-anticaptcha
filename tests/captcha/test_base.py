"""test base captcha"""

import pytest

from crawlerstack_anticaptcha.captcha import (CaptchaParser, NumericalCaptcha,
                                              SliderCaptcha)
from crawlerstack_anticaptcha.captcha.base import BaseCaptcha


def test_parse(mock_path):
    """test_parse"""
    base = BaseCaptcha(mock_path / 'foo')
    with pytest.raises(NotImplementedError):
        base.parse()


@pytest.mark.parametrize(
    'captcha',
    [
        'NumericalCaptcha',
        'SliderCaptcha'
    ]
)
def test_captcha_factory(mocker, mock_path, captcha):
    """test captcha factory"""
    mocker.patch.object(NumericalCaptcha, 'parse', return_value=1)
    mocker.patch.object(SliderCaptcha, 'parse', return_value=1)
    if captcha == 'SliderCaptcha':
        captcha = CaptchaParser('SliderCaptcha')
        res = captcha.factory(mock_path / 'foo', None, None)
        assert res == 1
    if captcha == 'NumericalCaptcha':
        captcha = CaptchaParser('NumericalCaptcha')
        num_res = captcha.factory(mock_path / 'foo', None, None)
        assert num_res == 1
    captcha = CaptchaParser('NumericalCaptcha')
    mocker.patch.object(NumericalCaptcha, 'parse', return_value='foo')
    res = captcha.factory(mock_path / 'foo', None, None)
    assert res == 'foo'
