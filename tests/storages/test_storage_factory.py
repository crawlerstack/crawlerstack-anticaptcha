"""test StorageFactory"""
import pytest

from crawlerstack_anticaptcha.storages import LocalStorages, Storage


@pytest.mark.parametrize(
    'storage_name',
    [
        # 'local',
        'test'
    ]
)
@pytest.mark.asyncio
async def test_get_default_storage(init_storage, storage_name):
    """test default"""
    if storage_name == 'local':
        storage = Storage(storage_name)
        await storage.get_default_storage()
        assert storage.storage.name == 'local'
        assert bool(storage.storage.default) is True
    if storage_name == 'test':
        storage = Storage(storage_name='test')
        storage.name = 'test'
        await storage.get_default_storage()
        assert storage.name == 'local'
        assert storage.storage.uri == 'foo'


@pytest.mark.asyncio
async def test_factory(mocker, init_storage):
    """test factory"""
    storage = Storage()
    mocker.patch.object(LocalStorages, 'save', return_value='foo')
    res = await storage.factory(b'1', 'foo', 'png')
    assert res == {'file': 'foo', 'id': 1}
