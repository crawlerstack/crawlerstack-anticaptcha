"""test StorageFactory"""
import pytest

from crawlerstack_anticaptcha.storages import Storage


@pytest.mark.parametrize(
    'storage_name',
    [
        'local',
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
        assert bool(storage.storage.default) is False
    if storage_name == 'test':
        storage = Storage()
        storage.name = 'test'
        await storage.get_default_storage()
        assert storage.name == 'test'
        assert storage.storage.uri == 'foo'


# @pytest.mark.asyncio
# async def test_factory(mocker, init_storage):
#     """test factory"""
#     storage = Storage()
#     storage.storage = StorageModel(id=1, name='test', uri='foo')
#     mocker.patch.object(LocalStorages, 'save', return_value='foo')
#     res = await storage.factory(b'1', 'foo', 'png')
#     assert res == {'file': 'foo', 'id': 1}
