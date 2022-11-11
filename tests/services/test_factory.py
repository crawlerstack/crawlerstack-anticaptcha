"""test factory"""

from crawlerstack_anticaptcha.captcha import captcha_factory
from crawlerstack_anticaptcha.captcha.numerical.captcha import NumericalCaptcha


def test_factory(mocker):
    """test factory"""
    test_file = mocker.MagicMock()
    mocker.patch.object(NumericalCaptcha, 'parse', return_value=1)
    result = captcha_factory('NumericalCaptcha', test_file)
    assert result == 1
