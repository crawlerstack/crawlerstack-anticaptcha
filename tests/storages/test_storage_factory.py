"""test StorageFactory"""
import pytest

from crawlerstack_anticaptcha.storages import LocalStorages, StorageFactory


@pytest.mark.asyncio
async def test_default():
    """test default"""
    storage = StorageFactory()
    await storage.default()
    assert storage.storage.id == 0


@pytest.mark.asyncio
async def test_factory(mocker):
    """test factory"""
    storage = StorageFactory()
    mocker.patch.object(LocalStorages, 'save', return_value='foo')
    res = await storage.factory(b'1', 'foo', 'png')
    assert res == {'file': 'foo', 'id': 0}
