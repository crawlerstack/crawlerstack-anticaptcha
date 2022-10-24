"""test factory"""

import pytest

from crawlerstack_anticaptcha.captcha import captcha_factory
from crawlerstack_anticaptcha.captcha.numerical.captcha import NumericalCaptcha
from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha


@pytest.mark.parametrize(
    'category',
    [
        'SliderCaptcha',
        'NumericalCaptcha',
        'test'
    ]
)
def test_factory(mocker, category):
    """test factory"""
    test_file = mocker.MagicMock()
    if category == 'SliderCaptcha':
        result = captcha_factory(category, test_file)
        assert isinstance(result, SliderCaptcha)
    if category == 'NumericalCaptcha':
        result = captcha_factory(category, test_file)
        assert isinstance(result, NumericalCaptcha)
    if category == 'test':
        result = captcha_factory(category, test_file)
        assert result is None
