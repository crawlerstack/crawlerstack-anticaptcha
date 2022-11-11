"""test CaptchaRecordRepository"""
import logging

import pytest

from crawlerstack_anticaptcha.models import (CaptchaFileModel,
                                             CaptchaRecordModel)
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


@pytest.mark.asyncio
async def test_create_record(caplog):
    """test create record"""
    record_repository = CaptchaRecordRepository()
    caplog.set_level(logging.DEBUG)
    result = await record_repository.create_record(
        CaptchaRecordModel(category_id=1, result=1),
        [CaptchaFileModel(filename='test', file_type='foo', storage_id=1)]
    )
    assert 'Create' in caplog.text
    assert result.id == 1


@pytest.mark.asyncio
async def test_update_by_pk(caplog, init_record):
    """test_update_by_pk"""
    record_repository = CaptchaRecordRepository()
    caplog.set_level(logging.DEBUG)
    await record_repository.update_by_pk(1, True)
    assert 'Update' in caplog.text
    res = await record_repository.get_by_id(1)
    assert res.success

    with pytest.raises(ObjectDoesNotExist):
        await record_repository.update_by_pk(5, True)
