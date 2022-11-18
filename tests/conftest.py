"""Test config"""
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from click.testing import CliRunner
from fastapi.testclient import TestClient
from fastapi_sa.database import db
from sqlalchemy.ext.asyncio import create_async_engine

from crawlerstack_anticaptcha.api.rest_api import app
from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.models import (Base, CaptchaCategoryModel,
                                             CaptchaFileModel,
                                             CaptchaRecordModel, StorageModel)
from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.repositories.storage import StorageRepository


@pytest.fixture
def mock_path() -> Path:
    """Mock a path, and clean when unit test done."""
    with TemporaryDirectory() as temp_path:
        yield Path(temp_path)


@pytest.fixture()
def clicker():
    """clicker fixture"""
    yield CliRunner()


@pytest.fixture(autouse=True, name='migrate')
async def migrate_fixture():
    """migrate fixture"""
    os.makedirs(Path(settings.DATABASE_URL.split('///')[1]).parent, exist_ok=True)
    _engine = create_async_engine(settings.DATABASE_URL)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await _engine.dispose()


@pytest.fixture(autouse=True)
async def db_init():
    """db_init"""
    db.init(settings.DATABASE_URL)


@pytest.fixture()
def db_session_ctx():
    """db session context"""
    token = db.set_session_ctx()
    yield
    db.reset_session_ctx(token)


@pytest.fixture()
async def session(db_session_ctx):
    """session fixture"""
    async with db.session.begin():
        yield db.session


@pytest.fixture()
def category_repository():
    """category repository fixture"""
    yield CategoryRepository()


@pytest.fixture(name='record_repository')
def record_repository_fixture():
    """record_repository_fixture"""
    yield CaptchaRecordRepository()


@pytest.fixture(name='storage_repository')
def storage_repository_fixture():
    """captcha_file_repository_fixture"""
    yield StorageRepository()


@pytest.fixture(name='init_category')
async def init_category_fixture(migrate):
    """init Category table data"""
    categories = [
        CaptchaCategoryModel(name='test')
    ]
    db.session.add_all(categories)
    await db.session.flush()


@pytest.fixture(name='init_record')
async def init_record_fixture(migrate):
    """init Category table data"""
    async with db():
        records = [
            CaptchaRecordModel(category_id=1, result='foo')
        ]
        db.session.add_all(records)
        await db.session.flush()


@pytest.fixture(name='init_storage')
async def init_storage_fixture(migrate):
    """init_storage"""
    async with db():
        storages = [
            StorageModel(name='local', uri='foo')
        ]
        db.session.add_all(storages)
        await db.session.flush()


@pytest.fixture(name='init_file_record')
async def init_file_record_fixture(migrate):
    """init_file_record"""
    async with db():
        files = [
            CaptchaFileModel(record_id=1, filename='foo', file_type='foo', storage_id=1),
            CaptchaFileModel(record_id=1, filename='bar', file_type='foo', storage_id=1),
        ]
        db.session.add_all(files)
        await db.session.flush()


@pytest.fixture(name='client')
def app_client_fixture():
    """app_client_fixture"""
    client = TestClient(app)
    yield client
