"""test base captcha"""

import pytest

from crawlerstack_anticaptcha.captcha import CaptchaParser, NumericalCaptcha
from crawlerstack_anticaptcha.captcha.base import BaseCaptcha


def test_parse(mock_path):
    """test_parse"""
    base = BaseCaptcha(mock_path / 'foo')
    with pytest.raises(NotImplementedError):
        base.parse()


def test_captcha_factory(mocker, mock_path):
    """test captcha factory"""
    captcha = CaptchaParser('NumericalCaptcha')
    mocker.patch.object(NumericalCaptcha, 'parse', return_value='foo')
    res = captcha.factory(mock_path / 'foo', None, None)
    assert res == 'foo'
