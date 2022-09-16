"""Test archive"""
import logging
import os
from pathlib import Path

import pytest

from crawlerstack_anticaptcha.repositories.mongo_repository import \
    MongoRepository
from crawlerstack_anticaptcha.services.archive import ArchiveService
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


def test_received_info(mocker):
    """
    test_received_info
    :param mocker:
    :return:
    """
    save_file = mocker.patch.object(ArchiveService, 'save_file', return_value='bar')
    test_file = mocker.MagicMock(content_type='foo')
    archive = ArchiveService(test_file, 'foo', 'false', 1)
    result = archive.received_info()
    save_file.assert_called_with()
    assert result.get('success') == 'false'
    assert result.get('file') == 'bar'


def test_written_to_db(mocker):
    """
    test_written_to_db
    :param mocker:
    :return:
    """
    write = mocker.patch.object(MongoRepository, 'write')
    test_file = mocker.MagicMock(content_type='foo')
    archive = ArchiveService(test_file, 'foo', 'false', 1)
    archive.received_info = mocker.MagicMock(return_value={'foo': 'bar'})
    archive.written_to_db()
    write.assert_called_with({'foo': 'bar'})


@pytest.mark.parametrize(
    'check',
    [
        True,
        False
    ]
)
def test_save_file(mocker, check):
    """
    test_save_file
    :param mocker:
    :return:
    """
    if check:
        mocker.patch.object(ArchiveService, 'check', return_value=check)
        mocker.patch.object(UploadedFile, 'save', return_value='bar')
        test_file = mocker.MagicMock(filename='foo.jpg')
        archive = ArchiveService(test_file, 'test', 'false', 1)
        result = archive.save_file()
        assert result == 'bar'
    if not check:
        mocker.patch.object(ArchiveService, 'check', return_value=check)
        mocker.patch.object(UploadedFile, 'save', return_value='bar')
        test_file = mocker.MagicMock(filename='foo.jpg')
        archive = ArchiveService(test_file, 'test', 'false', 1)
        result = archive.save_file()
        assert result == 'File already exists.'


@pytest.mark.parametrize(
    'archive',
    [
        True,
        False
    ]
)
def test_check(mock_path, caplog, archive):
    """
    test_check
    :param mock_path:
    :param caplog:
    :param archive:
    :return:
    """
    archive = ArchiveService('test', b'1', 'false', 1)
    archive.image_save_path = mock_path
    if archive:
        assert archive.check(b'1')
    if not archive:
        os.makedirs(Path(f'{mock_path}/Archive'))
        with open(Path(f'{mock_path}/Archive/test.png'), 'wb') as file:
            file.write(b'2')
        caplog.set_level(logging.INFO)
        assert not archive.check(b'2')
        assert 'already exists' in caplog.text
