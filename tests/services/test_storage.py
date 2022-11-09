"""test storage"""
import datetime

import pytest

from crawlerstack_anticaptcha.models import StorageModel
from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.services.storage import StorageService
from crawlerstack_anticaptcha.utils.schema import Message


@pytest.mark.asyncio
async def test_create(mocker):
    """test create"""
    create = mocker.patch.object(StorageRepository, 'create')
    storage = StorageService(storage_id=1, name='foo', uri='test')
    storage.now = datetime.datetime(2022, 1, 1, 1, 1)
    result = await storage.create()
    create.assert_called()
    assert result.code == 200


@pytest.mark.asyncio
async def test_update(mocker):
    """test_update"""
    update_by_id = mocker.patch.object(StorageRepository, 'update_by_id')
    storage = StorageService(storage_id=1, default=True)
    result = await storage.update()
    update_by_id.assert_called_with(1, True)
    assert result == Message(code=200, data=None, message='ok')


@pytest.mark.asyncio
async def test_get_all(mocker):
    """test_get_all"""
    mocker.patch.object(StorageRepository, 'get_all', return_value=[StorageModel(id=1, name='foo', uri='foo')])
    storage = StorageService()
    result = await storage.get_all()
    assert result == Message(code=200, data=[{'id': 1, 'name': 'foo', 'uri': 'foo'}],
                             message='Available storage methods.')


@pytest.mark.asyncio
async def test_get_by_id(mocker):
    """test_get_by_id"""
    mocker.patch.object(StorageRepository, 'get_by_id', return_value=None)
    storage = StorageService(storage_id=1)
    result = await storage.get_by_id()
    assert result == Message(code=200, data=None, message='Details with id 1')


@pytest.mark.asyncio
async def test_delete_by_id(mocker):
    """test_delete_by_id"""
    delete_by_id = mocker.patch.object(StorageRepository, 'delete_by_id')
    storage = StorageService(storage_id=1)
    result = await storage.delete_by_id()
    delete_by_id.assert_called_with(1)
    assert result == Message(code=200, data=None, message='ok')
