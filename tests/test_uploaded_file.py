"""Test uploaded file"""
import logging
from enum import EnumMeta
from pathlib import Path

import pytest

from crawlerstack_anticaptcha.utils.upload_file import UploadedFile


@pytest.fixture(name='mock_path')
def fixture_mock_file_path(mock_path) -> Path:
    """
    fixture_mock_file_path
    :param mock_path:
    :return:
    """
    test_path = mock_path
    yield test_path


def test_save(mocker, mock_path):
    """
    test_save
    :param mocker:
    :param mock_path:
    :return:
    """
    upload_file = UploadedFile(b'foo', 'foo', 'bar.txt')
    upload_file.image_save_path = mock_path
    write_to_file = mocker.patch.object(UploadedFile, 'write_to_file')
    upload_file.save()
    write_to_file.assert_called()


def test_write_to_file(mocker, mock_path, caplog):
    """
    test_write_to_file
    :param mock_path:
    :param caplog:
    :return:
    """
    caplog.set_level(logging.INFO)
    value = mocker.MagicMock(value=mock_path)
    test_category = mocker.MagicMock(
        SAVE_PATH=value,
        return_value=EnumMeta
    )
    upload_file = UploadedFile(b'1', test_category, 'test.dat')
    result = upload_file.write_to_file()
    with open(mock_path / 'test.dat', 'rb') as obj:
        assert obj.read() == b'1'
    assert 'Save Complete' in caplog.text
    assert 'test.dat' in str(result)
