"""Test Captcha Service"""

import pytest

from crawlerstack_anticaptcha.models import CategoryModel
from crawlerstack_anticaptcha.repositories.respositorie import \
    CaptchaRepository
from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.slider_captcha.captcha import SliderCaptcha
from crawlerstack_anticaptcha.utils.exception import (ObjectDoesNotExist,
                                                      SliderCaptchaParseFailed,
                                                      UnsupportedMediaType)
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
        CaptchaService,
        'get_category',
        return_value=CategoryModel(path='test', id=1, name='foo')
    )
    save_file = mocker.patch.object(CaptchaService, 'save_file')
    parse = mocker.patch.object(CaptchaService, 'parse', return_value=1)
    write_to_db = mocker.patch.object(CaptchaService, 'write_to_db')
    if 'image' in file_type:
        file = mocker.MagicMock(content_type=file_type)
        captcha_service = CaptchaService(file, 'foo', b'1')
        captcha_service.file_uuid = '1'
        result = await captcha_service.check()
        assert result.code == 200
        save_file.assert_called()
        parse.assert_called()
        write_to_db.assert_called()
    if 'test' in file_type:
        file = mocker.MagicMock(content_type=file_type)
        captcha_service = CaptchaService(file, 'foo', b'1')
        with pytest.raises(UnsupportedMediaType):
            await captcha_service.check()


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
        result = await captcha.get_category()
        assert result.id == 1
    else:
        captcha = CaptchaService(mocker.MagicMock(), category, mocker.MagicMock())
        with pytest.raises(ObjectDoesNotExist):
            await captcha.get_category()


@pytest.mark.asyncio
async def test_save_file(mocker, mock_path):
    """test save file"""
    save = mocker.patch.object(UploadedFile, 'save')
    test_file = mock_path / 'foo.jpg'
    captcha_ser = CaptchaService(mocker.MagicMock(), 'test', b'1')
    await captcha_ser.save_file(test_file)
    save.assert_called()


@pytest.mark.parametrize(
    'parse_result',
    [
        1,
        0
    ]
)
@pytest.mark.asyncio
async def test_parse(mocker, parse_result, mock_path):
    """test parse"""
    write_to_db = mocker.patch.object(CaptchaService, 'write_to_db')
    test_file = mock_path / 'foo.jpg'
    captcha_ser = CaptchaService(mocker.MagicMock(), 'test', b'1')
    if parse_result == 0:
        mocker.patch.object(SliderCaptcha, 'parse', return_value=parse_result)
        captcha_ser.file_uuid = 'foo'
        with pytest.raises(SliderCaptchaParseFailed):
            await captcha_ser.parse(test_file, 1)
            write_to_db.assert_called_with(
                {'category_id': 1,
                 'file_id': 'foo',
                 'file_type': 'jpg',
                 'success': False}
            )
    if parse_result == 1:
        mocker.patch.object(SliderCaptcha, 'parse', return_value=parse_result)
        assert await captcha_ser.parse(test_file, 1) == 1
