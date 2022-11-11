"""test update record"""
import pytest

from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.services.update_record import UpdateRecordService


@pytest.mark.asyncio
async def test_update(mocker):
    """test_update"""
    update_by_pk = mocker.patch.object(CaptchaRecordRepository, 'update_by_pk')
    update_record = UpdateRecordService(True, 'test')
    await update_record.update()
    update_by_pk.assert_called_with('test', True)
