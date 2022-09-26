"""test update record"""
import pytest

from crawlerstack_anticaptcha.repositories.respositories import \
    CaptchaRepository
from crawlerstack_anticaptcha.services.update_record import UpdateRecordService


@pytest.mark.asyncio
async def test_update(mocker):
    """test_update"""
    update_by_file_id = mocker.patch.object(CaptchaRepository, 'update_by_file_id')
    update_record = UpdateRecordService(True, 'test')
    await update_record.update()
    update_by_file_id.assert_called_with('test', True)
