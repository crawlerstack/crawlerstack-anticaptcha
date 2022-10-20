"""test factory"""
from pathlib import Path

import pytest

from crawlerstack_anticaptcha.captcha.numerical.captcha import NumCaptcha
from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha
from crawlerstack_anticaptcha.repositories.respositorie import \
    CaptchaRepository
from crawlerstack_anticaptcha.services import (CaptchaFactory,
                                               NumericalCaptchaService,
                                               RotatedCaptchaService,
                                               SliderCaptchaService)
from crawlerstack_anticaptcha.utils.exception import (
    NumericalCaptchaParseFailed, SliderCaptchaParseFailed)


@pytest.mark.parametrize(
    'category',
    [
        'SliderCaptcha',
        'NumericalCaptcha',
        'RotatedCaptcha'
    ]
)
def test_factory(mocker, category):
    """test factory"""
    test_file = mocker.MagicMock()
    if category == 'SliderCaptcha':
        result = CaptchaFactory.captcha(category, test_file, 1, 'foo')
        assert isinstance(result, SliderCaptchaService)
    if category == 'NumericalCaptcha':
        result = CaptchaFactory.captcha(category, test_file, 1, 'foo')
        assert isinstance(result, NumericalCaptchaService)
    if category == 'RotatedCaptcha':
        result = CaptchaFactory.captcha(category, test_file, 1, 'foo')
        assert isinstance(result, RotatedCaptchaService)


@pytest.mark.parametrize(
    'result',
    [
        1,
        0
    ]
)
@pytest.mark.asyncio
async def test_slider_parse(mocker, result):
    """test_slider_parse"""
    slider_captcha = SliderCaptchaService(Path('/test/foo.png'), 1, 'foo')
    create = mocker.patch.object(CaptchaRepository, 'create')
    if result:
        mocker.patch.object(SliderCaptcha, 'parse', return_value=result)
        res = await slider_captcha.parse()
        assert res == 1
    else:
        mocker.patch.object(SliderCaptcha, 'parse', return_value=result)
        with pytest.raises(SliderCaptchaParseFailed):
            await slider_captcha.parse()
            create.assert_called_with(
                {'category_id': 1, 'file_id': 'foo', 'file_type': 'png', 'success': False}
            )


@pytest.mark.parametrize(
    'result',
    [
        'test',
        'foo'
    ]
)
@pytest.mark.asyncio
async def test_numerical_parse(mocker, result):
    """test_numerical_parse"""
    num_captcha = NumericalCaptchaService(Path('/test/foo.png'), 1, 'foo')
    create = mocker.patch.object(CaptchaRepository, 'create')
    if len(result) < 4:
        mocker.patch.object(NumCaptcha, 'parse', return_value=result)
        with pytest.raises(NumericalCaptchaParseFailed):
            await num_captcha.parse()
            create.assert_called_with(
                {'category_id': 1, 'file_id': 'foo', 'file_type': 'png', 'success': False}
            )
    else:
        mocker.patch.object(NumCaptcha, 'parse', return_value=result)
        res = await num_captcha.parse()
        assert res == 'test'
