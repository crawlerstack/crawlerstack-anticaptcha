"""test CaptchaRecordRepository"""
import logging
from datetime import datetime

import pytest

from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


@pytest.mark.asyncio
async def test_create_record(caplog):
    """test create record"""
    record_repository = CaptchaRecordRepository()
    caplog.set_level(logging.DEBUG)
    result = await record_repository.create_record(
        category_id=1,
        result=100,
        success=True,
        create_time=datetime(2022, 1, 1)
    )
    assert 'Create' in caplog.text
    assert result == 1


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
