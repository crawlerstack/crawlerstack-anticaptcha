"""test local"""
import logging

import pytest

from crawlerstack_anticaptcha.models import StorageModel
from crawlerstack_anticaptcha.storages import LocalStorages


@pytest.mark.asyncio
async def test_save(mock_path, mocker):
    """test save"""
    write_to_file = mocker.patch.object(LocalStorages, 'write_to_file')
    local = LocalStorages(StorageModel(uri=str(mock_path)))
    result = await local.save('foo', 'png', b'1')
    assert result == mock_path / 'foo.png'
    write_to_file.assert_called_with(mock_path / 'foo.png', b'1')


@pytest.mark.asyncio
async def test_save_not_found(mock_path):
    """test_save_not_found"""
    local = LocalStorages(StorageModel(uri=str(mock_path / 'test')))
    result = await local.save('foo', 'png', b'1')
    assert result == mock_path / 'test/foo.png'


def test_write_to_file(mocker, mock_path, caplog):
    """test write_to_file"""
    test_file = mock_path / 'foo.png'
    local = LocalStorages(mocker.MagicMock())
    caplog.set_level(logging.DEBUG)
    local.write_to_file(test_file, b'1')
    assert f'Save file to {test_file}' in caplog.text
    with open(test_file, 'rb') as obj:
        assert obj.read() == b'1'
