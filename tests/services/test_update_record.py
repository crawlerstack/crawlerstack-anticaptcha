"""test update record"""
import pytest

from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.services.update_record import UpdateRecordService


@pytest.mark.asyncio
async def test_update(mocker):
    """test_update"""
    update_by_id = mocker.patch.object(CaptchaRecordRepository, 'update_by_id')
    update_record = UpdateRecordService(True, 'test')
    await update_record.update()
    update_by_id.assert_called_with('test', success=True)
