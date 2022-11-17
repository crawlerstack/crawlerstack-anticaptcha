"""Test config"""
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from click.testing import CliRunner
from fastapi.testclient import TestClient
from fastapi_sa.database import db, session_ctx

from crawlerstack_anticaptcha.api.rest_api import app
from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.models import (CaptchaCategoryModel,
                                             CaptchaFileModel,
                                             CaptchaRecordModel, StorageModel)
from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.repositories.storage import StorageRepository

collect_ignore = ["../tests/repository"]
db.init(url=settings.DATABASE_URL)


@pytest.fixture
def mock_path() -> Path:
    """Mock a path, and clean when unit test done."""
    with TemporaryDirectory() as temp_path:
        yield Path(temp_path)


@pytest.fixture()
def clicker():
    """clicker fixture"""
    yield CliRunner()


@pytest.fixture(name='category_repository')
def category_repository_fixture():
    """category repository fixture"""
    category_repository = CategoryRepository()
    yield category_repository


@pytest.fixture(name='record_repository')
def record_repository_fixture():
    """record_repository_fixture"""
    record_repository = CaptchaRecordRepository()
    yield record_repository


@pytest.fixture(name='storage_repository')
def storage_repository_fixture():
    """captcha_file_repository_fixture"""
    storage_repository = StorageRepository()
    yield storage_repository


@pytest.fixture(name='init_category')
def init_category_fixture():
    """init Category table data"""
    categories = [
        CaptchaCategoryModel(name='test')
    ]
    db.session.add_all(categories)


@pytest.fixture(name='init_record')
async def init_record_fixture():
    """init Category table data"""
    records = [
        CaptchaRecordModel(category_id=1, result='foo')
    ]
    db.session.add_all(records)


@pytest.fixture(name='init_storage')
@session_ctx
async def init_storage_fixture():
    """init_storage"""
    storages = [
        StorageModel(name='local', uri='foo', )
    ]
    db.session.add_all(storages)


@pytest.fixture(name='init_file_record')
@session_ctx
async def init_file_record_fixture():
    """init_file_record"""
    async with db() as session:
        files = [
            CaptchaFileModel(record_id=1, filename='foo', file_type='foo', storage_id=1),
            CaptchaFileModel(record_id=1, filename='bar', file_type='foo', storage_id=1),
        ]
        session.add_all(files)


@pytest.fixture(name='client')
def app_client_fixture():
    """app_client_fixture"""
    client = TestClient(app)
    yield client
