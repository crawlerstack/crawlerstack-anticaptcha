"""test storage repository"""
import logging
from datetime import datetime

import pytest

from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


@pytest.mark.asyncio
async def test_update_by_id(init_storage, caplog):
    """test update by id"""
    storage = StorageRepository()
    caplog.set_level(logging.INFO)
    await storage.update_by_id(1, False)
    assert 'Update' in caplog.text
    res = await storage.get_by_id(1)
    assert not res.default
    assert res.update_time.date() == datetime.now().date()

    with pytest.raises(ObjectDoesNotExist):
        await storage.update_by_id(5, False)


@pytest.mark.asyncio
async def test_get_default(init_storage):
    """test get default"""
    storage = StorageRepository()
    result = await storage.get_default()
    assert result.name == 'test'
