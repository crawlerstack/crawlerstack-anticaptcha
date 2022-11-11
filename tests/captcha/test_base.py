"""test base captcha"""

import pytest

from crawlerstack_anticaptcha.captcha import NumericalCaptcha, captcha_factory
from crawlerstack_anticaptcha.captcha.base import BaseCaptcha


def test_parse(mock_path):
    """test_parse"""
    base = BaseCaptcha(mock_path / 'foo')
    with pytest.raises(NotImplementedError):
        base.parse()


def test_captcha_factory(mocker, mock_path):
    """test captcha factory"""
    mocker.patch.object(NumericalCaptcha, 'parse', return_value='foo')
    res = captcha_factory('NumericalCaptcha', mock_path / 'foo')
    assert res == 'foo'
