"""test CaptchaRecordRepository"""
import logging

import pytest

from crawlerstack_anticaptcha.models import (CaptchaFileModel,
                                             CaptchaRecordModel)


def test_model(record_repository):
    """test model"""
    res = record_repository.model
    assert res == CaptchaRecordModel


@pytest.mark.asyncio
async def test_create_record(record_repository, caplog, session):
    """test create record"""
    caplog.set_level(logging.DEBUG)
    result = await record_repository.create_record(
        CaptchaRecordModel(id=1, category_id=1, result=1),
        [CaptchaFileModel(id=1, filename='test', file_type='foo', storage_id=1)]
    )
    assert 'Create' in caplog.text
    assert result.id == 1
