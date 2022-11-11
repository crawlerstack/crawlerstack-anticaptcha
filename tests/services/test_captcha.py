"""Test Captcha Service"""

import pytest
from fastapi import File

from crawlerstack_anticaptcha.captcha import NumericalCaptcha
from crawlerstack_anticaptcha.models import StorageModel
from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.services.captcha import (CaptchaService,
                                                       storage_default)
from crawlerstack_anticaptcha.utils.schema import Captcha


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
async def test_parse(mocker, mock_path):
    """test parse"""
    captcha = CaptchaService(image=mocker.MagicMock(return_value=File), category=Captcha.Numerical.value)
    mocker.patch.object(NumericalCaptcha, 'parse', return_value=1)
    result = await captcha.parse(mocker.MagicMock())
    assert result == 1

    mocker.patch.object(NumericalCaptcha, 'parse', return_value=0)
    result = await captcha.parse(mocker.MagicMock())
    assert not result
