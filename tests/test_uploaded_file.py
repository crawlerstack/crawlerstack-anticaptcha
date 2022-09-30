"""Test uploaded file"""
import logging
from pathlib import Path

import pytest

from crawlerstack_anticaptcha.utils.upload_file import UploadedFile


@pytest.mark.asyncio
async def test_save(mocker, mock_path):
    """
    test_save
    :param mocker:
    :param mock_path:
    :return:
    """
    test_file = mock_path / 'foo.txt'
    upload_file = UploadedFile(b'foo', test_file)
    write_to_file = mocker.patch.object(UploadedFile, 'write_to_file')
    await upload_file.save()
    write_to_file.assert_called()


@pytest.mark.asyncio
async def test_save_not_fount(mock_path):
    """test error situation"""
    test_file = mock_path / 'test' / 'foo.txt'
    upload_file = UploadedFile(b'foo', test_file)
    await upload_file.save()
    assert Path(test_file).parent.exists()


def test_write_to_file(mock_path, caplog):
    """
    test_write_to_file
    :param mock_path:
    :param caplog:
    :return:
    """
    test_file = mock_path / 'foo.txt'
    with caplog.at_level(logging.DEBUG):
        upload_file = UploadedFile(b'1', test_file)
        upload_file.write_to_file()
        assert 'Save file' in caplog.text
    with open(test_file, 'rb') as obj:
        assert obj.read() == b'1'
