"""test base captcha"""

import pytest

from crawlerstack_anticaptcha.captcha.base import BaseCaptcha


def test_parse(mock_path):
    """test_parse"""
    base = BaseCaptcha(mock_path / 'foo')
    with pytest.raises(NotImplementedError):
        base.parse()
