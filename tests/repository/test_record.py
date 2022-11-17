"""test CaptchaRecordRepository"""
import logging

import pytest

from crawlerstack_anticaptcha.models import (CaptchaFileModel,
                                             CaptchaRecordModel)


@pytest.mark.asyncio
async def test_create_record(record_repository, caplog):
    """test create record"""
    caplog.set_level(logging.DEBUG)
    result = await record_repository.create_record(
        CaptchaRecordModel(category_id=1, result=1),
        [CaptchaFileModel(filename='test', file_type='foo', storage_id=1)]
    )
    assert 'Create' in caplog.text
    assert result.id == 1


@pytest.mark.asyncio
async def test_update_by_id(record_repository, caplog, init_record):
    """test_update_by_pk"""
    caplog.set_level(logging.DEBUG)
    await record_repository.update_by_id(1, success=True)
    assert 'Update' in caplog.text
    res = await record_repository.get_by_id(1)
    assert res.success is True
