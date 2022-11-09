"""Test Captcha Service"""
import datetime
from pathlib import Path

import pytest
from fastapi import File

from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha
from crawlerstack_anticaptcha.models import StorageModel
from crawlerstack_anticaptcha.repositories.file import CaptchaFileRepository
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.services.captcha import (CaptchaService,
                                                       storage_default)
from crawlerstack_anticaptcha.utils.schema import Captcha
from crawlerstack_anticaptcha.utils.upload_file import UploadedFile


@pytest.mark.asyncio
async def test_save(mocker, mock_path):
    """test save file"""
    save = mocker.patch.object(UploadedFile, 'save')
    test_file = mock_path / 'foo.jpg'
    await save(b'1', test_file)
    save.assert_called_with(b'1', mock_path / 'foo.jpg')


@pytest.mark.asyncio
async def test_storage_default(mocker):
    """test_storage_default"""
    mocker.patch.object(
        StorageRepository,
        'get_default',
        return_value=StorageModel(
            uri='foo',
            name='test'
        )
    )
    res = await storage_default()
    assert res.name == 'test'


@pytest.mark.asyncio
async def test_check_category(mocker):
    """test_check_category"""
    image = mocker.MagicMock(return_value=File)
    captcha = CaptchaService(image=image, category=Captcha.Slider.value)
    captcha.file_uuid = 'test'
    res = await captcha.check_category('foo', mocker.MagicMock(return_vaule=File(), content_type='image/jpg'))
    assert res == Path('foo/slider-captcha/test.jpg')

    captcha = CaptchaService(image=image, category=Captcha.Numerical.value)
    captcha.file_uuid = 'test'
    res = await captcha.check_category('foo', mocker.MagicMock(return_vaule=File(), content_type='image/jpg'))
    assert res == Path('foo/numerical-captcha/test.jpg')


@pytest.mark.asyncio
async def test_written_to_db(mocker):
    """test written_to_db"""
    mocker.patch.object(CaptchaRecordRepository, 'create', return_value=1)
    file_create = mocker.patch.object(CaptchaFileRepository, 'create')
    image = mocker.MagicMock(return_value=File)
    captcha = CaptchaService(image=image, category=Captcha.Slider.value)
    captcha.now = datetime.datetime(2022, 1, 1)
    res = await captcha.write_to_db(1, 'foo', None, 'res', 'foo', 1)
    file_create.assert_called()
    assert res == 1


@pytest.mark.asyncio
async def test_parse(mocker, mock_path):
    """test parse"""
    captcha = CaptchaService(image=mocker.MagicMock(return_value=File), category=Captcha.Slider.value)
    mocker.patch.object(SliderCaptcha, 'parse', return_value=1)
    result = await captcha.parse(mocker.MagicMock())
    assert result == 1

    mocker.patch.object(SliderCaptcha, 'parse', return_value=0)
    result = await captcha.parse(mocker.MagicMock())
    assert not result
