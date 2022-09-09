"""Test uploaded file"""
import logging
import os
from pathlib import Path

import pytest

from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


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

    upload_file.download_path = mock_path
    write_to_file = mocker.patch.object(UploadedFile, 'write_to_file')
    upload_file.save()
    write_to_file.assert_called()


def test_write_to_file(mock_path, caplog):
    """
    test_write_to_file
    :param mock_path:
    :param caplog:
    :return:
    """
    caplog.set_level(logging.INFO)
    upload_file = UploadedFile(b'1', 'foo', 'test.dat')
    os.mkdir(Path(mock_path / 'foo'))
    upload_file.download_path = mock_path
    upload_file.write_to_file()
    with open(mock_path / 'foo/test.dat', 'rb') as obj:
        assert obj.read() == b'1'
    assert 'Download Complete' in caplog.text
