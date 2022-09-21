"""Test handler"""

import pytest

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.repositories.respositories import (
    CaptchaRepository, CategoryRepository)
from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


@pytest.mark.parametrize(
    'test_file,category_name',
    [
        ('image', 'SliderCaptcha'),
        ('image', 'RotatedCaptcha'),
        ('foo', 'foo'),
        ('foo', 'bar')
    ]
)
@pytest.mark.asyncio
async def test_check(mocker, test_file, category_name):
    """test check"""
    if test_file != 'image':
        test_file = mocker.MagicMock(content_type=test_file, filename='foo.jpg')
        file_data = mocker.MagicMock()
        captcha_service = CaptchaService(test_file, category_name, file_data)
        result = await captcha_service.check()
        assert result.data is None

    if test_file == 'image' and category_name == 'SliderCaptcha':
        written_to_db = mocker.patch.object(CaptchaService, 'written_to_db')
        save = mocker.patch.object(UploadedFile, 'save')
        parse = mocker.patch.object(SliderCaptcha, 'parse')
        test_file = mocker.MagicMock(content_type=test_file, filename='foo.jpg')
        file_data = mocker.MagicMock()
        captcha_service = CaptchaService(test_file, category_name, file_data)
        result = await captcha_service.check()
        save.assert_called()
        parse.assert_called()
        written_to_db.assert_called()
        assert result.code == 200
        assert 'succeeded' in result.message

    if test_file == 'image' and category_name == 'RotatedCaptcha':
        written_to_db = mocker.patch.object(CaptchaService, 'written_to_db')
        save = mocker.patch.object(UploadedFile, 'save')
        parse = mocker.patch.object(SliderCaptcha, 'parse')
        test_file = mocker.MagicMock(content_type=test_file, filename='foo.jpg')
        file_data = mocker.MagicMock()
        captcha_service = CaptchaService(test_file, category_name, file_data)
        result = await captcha_service.check()
        assert result.code == 200
        written_to_db.assert_called()
        save.assert_called()
        parse.assert_called()

    else:
        test_file = mocker.MagicMock(content_type=test_file, filename='foo.jpg')
        file_data = mocker.MagicMock()
        captcha_service = CaptchaService(test_file, category_name, file_data)
        result = await captcha_service.check()
        assert result.code == 415


@pytest.mark.asyncio
async def test_written_to_db(mocker):
    """test written_to_db"""
    create = mocker.patch.object(CaptchaRepository, 'create')
    captcha_service = CaptchaService('test', 'foo', mocker.MagicMock())
    await captcha_service.written_to_db()
    create.assert_called_with()


@pytest.mark.asyncio
async def test_init_category(mocker):
    """test init category"""
    add_all = mocker.patch.object(CategoryRepository, 'add_all')
    captcha_service = CaptchaService('test', 'foo', 'data')
    await captcha_service.init_category()
    add_all.assert_called()
