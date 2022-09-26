"""Test"""

import pytest
from fastapi import File

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.models import CategoryModel
from crawlerstack_anticaptcha.repositories.respositories import (
    CaptchaRepository, CategoryRepository)
from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist
from crawlerstack_anticaptcha.utils.upload_file import UploadedFile


@pytest.mark.parametrize(
    'file_type',
    [
        'image/foo',
        'test',
    ]
)
@pytest.mark.asyncio
async def test_check(mocker, file_type):
    """test check"""
    mocker.patch.object(
        CategoryRepository,
        'get_by_id',
        return_value=mocker.MagicMock(type='SliderCaptcha')
    )
    if 'image' in file_type:
        parse = mocker.patch.object(SliderCaptcha, 'parse')
        save = mocker.patch.object(UploadedFile, 'save')
        write_to_db = mocker.patch.object(CaptchaService, 'write_to_db')
        mocker.patch.object(
            CategoryRepository,
            'get_by_name',
            return_value=CategoryModel(name='SliderCategory', path='test', id=1
                                       )
        )
        test_file = mocker.MagicMock(
            content_type=file_type,
            file_name='foo.jpg',
            return_value=File
        )
        data = mocker.MagicMock()
        captcha_service = CaptchaService(test_file, 'SliderCategory', data)
        result = await captcha_service.check()
        save.assert_called()
        parse.assert_called()
        write_to_db.assert_called()
        assert result.code == 200
    if 'test' in file_type:
        mocker.patch.object(
            CategoryRepository,
            'get_by_name',
            return_value=CategoryModel(
                name='SliderCategory', path='test', id=1)
        )
        test_file = mocker.MagicMock(
            content_type=file_type,
            file_name='foo.jpg'
        )
        data = mocker.MagicMock()
        captcha_service = CaptchaService(test_file, 'test', data)
        result = await captcha_service.check()
        assert result.code == 415


@pytest.mark.asyncio
async def test_written_to_db(mocker):
    """test written_to_db"""
    create = mocker.patch.object(CaptchaRepository, 'create')
    captcha_service = CaptchaService('test', 'foo', mocker.MagicMock())
    await captcha_service.write_to_db()
    create.assert_called_with()


@pytest.mark.parametrize(
    'category',
    [
        'test',
        'SliderCaptcha'
    ]
)
@pytest.mark.asyncio
async def test_check_category(init_category, category, mocker):
    """test check category"""
    if category == 'SliderCaptcha':
        captcha = CaptchaService('test', category, mocker.MagicMock())
        result = await captcha.check_category()
        assert result.id == 1
    else:
        captcha = CaptchaService(mocker.MagicMock(), category, mocker.MagicMock())
        with pytest.raises(ObjectDoesNotExist):
            await captcha.check_category()
