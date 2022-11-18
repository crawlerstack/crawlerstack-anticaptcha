"""test captcha service"""

import pytest

from crawlerstack_anticaptcha.captcha import CaptchaParser
from crawlerstack_anticaptcha.models import CaptchaCategoryModel
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.services.captcha import CaptchaService


@pytest.mark.asyncio
async def test_parse(mocker):
    """test parse"""
    test_image = mocker.MagicMock()
    factory = mocker.patch.object(CaptchaParser, 'factory')
    captcha_service = CaptchaService(bg_image=test_image, category='test')
    await captcha_service.parse({'file': 'foo'})
    factory.assert_called_with('foo', None, None)

    captcha_service = CaptchaService(bg_image=test_image, category='test', fore_image=test_image)
    await captcha_service.parse({'file': 'foo'})
    factory.assert_called_with('foo', None, None)


@pytest.mark.asyncio
async def test_parse_res(mocker):
    """test_parse_res"""
    test_image = mocker.MagicMock()
    mocker.patch.object(CaptchaParser, 'factory', return_value=1)
    captcha_service = CaptchaService(bg_image=test_image, category='test')
    assert await captcha_service.parse({'file': 'foo'}) == 1


@pytest.mark.asyncio
async def test_single_img_record(mocker):
    """test_single_img_record"""
    create_record = mocker.patch.object(CaptchaRecordRepository, 'create_record')
    test_image = mocker.MagicMock()
    category = CaptchaCategoryModel(id=1)
    captcha_service = CaptchaService(bg_image=test_image, category='test', fore_image=test_image)
    await captcha_service.image_record(
        category=category,
        parse_result=1,
        file_info=[{'file': 'file', 'file_name': 'file_name', 'file_type': 'file_type', 'id': 'id'}],
    )
    create_record.assert_called()


@pytest.mark.asyncio
async def test_multi_img_record(mocker):
    """test_multi_img_record"""
    create_record = mocker.patch.object(CaptchaRecordRepository, 'create_record')
    test_image = mocker.MagicMock()
    category = CaptchaCategoryModel(id=1)
    captcha_service = CaptchaService(bg_image=test_image, category='test', fore_image=test_image)
    await captcha_service.image_record(
        category=category,
        parse_result=1,
        file_info=({'id': 1}, {'id': 1}),
    )
    create_record.assert_called()
