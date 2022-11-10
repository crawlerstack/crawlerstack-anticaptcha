"""test file record"""
import pytest


@pytest.mark.asyncio
async def test_get_by_record_id(init_file_record, captcha_file_repository):
    """test_get_by_record_id"""
