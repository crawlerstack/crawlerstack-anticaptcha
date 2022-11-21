"""test storage repository"""
import logging

import pytest

from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


@pytest.mark.asyncio
async def test_update_by_id(storage_repository, init_storage, caplog, session):
    """test update by id"""
    caplog.set_level(logging.DEBUG)
    await storage_repository.update_by_id(1, default=False)
    assert 'Update' in caplog.text
    res = await storage_repository.get_by_id(1)
    assert not res.default


@pytest.mark.asyncio
async def test_init_default(storage_repository, init_storage, session):
    """test_init_default"""
    await storage_repository.init_default()
    res = await storage_repository.get_by_name('local')
    assert bool(res.default) is False


@pytest.mark.asyncio
async def test_get_by_name(storage_repository, init_storage, session):
    """test get default"""
    result = await storage_repository.get_by_name('local')
    assert result.uri == 'foo'


@pytest.mark.asyncio
async def test_update_by_name(storage_repository, init_storage, session):
    """test_update_by_name"""
    await storage_repository.update_by_name('local')
    res = await storage_repository.get_by_name('local')
    assert bool(res.default) is True

    with pytest.raises(ObjectDoesNotExist):
        await storage_repository.update_by_name('test')
