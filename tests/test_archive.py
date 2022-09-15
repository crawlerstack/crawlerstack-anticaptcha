"""Test archive"""
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
        assert result == ''
