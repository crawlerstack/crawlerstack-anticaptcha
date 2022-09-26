"""Test uploaded file"""
import logging
from pathlib import Path

import pytest

from crawlerstack_anticaptcha.repositories.models import CategoryModel
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
    upload_file = UploadedFile(b'foo', mocker.MagicMock(), 'bar.txt')
    upload_file.image_save_path = mock_path
    write_to_file = mocker.patch.object(UploadedFile, 'write_to_file')
    upload_file.save()
    write_to_file.assert_called()


def test_write_to_file(mocker, mock_path, caplog):
    """
    test_write_to_file
    :param mocker:
    :param mock_path:
    :param caplog:
    :return:
    """
    caplog.set_level(logging.INFO)
    test_category = mocker.MagicMock(
        path=mock_path,
        return_value=CategoryModel
    )
    upload_file = UploadedFile(b'1', test_category, 'test.dat')
    result = upload_file.write_to_file()
    with open(Path(result), 'rb') as obj:
        assert obj.read() == b'1'
    assert 'Save Complete' in caplog.text
    assert 'test.dat' in str(result)
