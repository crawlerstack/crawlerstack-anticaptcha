"""Test config"""
import asyncio
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from click.testing import CliRunner
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from crawlerstack_anticaptcha import config
from crawlerstack_anticaptcha.api.rest_api import app
from crawlerstack_anticaptcha.models import (BaseModel, CaptchaCategoryModel,
                                             CaptchaFileModel,
                                             CaptchaRecordModel, StorageModel)
from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.repositories.file import CaptchaFileRepository
from crawlerstack_anticaptcha.repositories.storage import StorageRepository


@pytest.fixture(name='settings')
def settings_fixture():
    """settings fixture"""
    return config.settings


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


@pytest.fixture(name='captcha_repository')
def captcha_repository_fixture():
    """captcha repository fixture"""
    captcha_repository = CategoryRepository()
    yield captcha_repository


@pytest.fixture(name='storage_repository')
def storage_repository_fixture():
    """captcha_file_repository_fixture"""
    storage_repository = StorageRepository()
    yield storage_repository


@pytest.fixture(name='captcha_file_repository')
def captcha_file_repository_fixture():
    """captcha_file_repository_fixture"""
    captcha_file_repository = CaptchaFileRepository()
    yield captcha_file_repository


@pytest.fixture(autouse=True, name='migrate')
def migrate_fixture(settings):
    """migrate fixture"""

    async def setup():
        """setup"""
        db_path = Path(settings.DATABASE_URL.split('///')[1]).parent
        if not db_path.exists():
            os.makedirs(db_path)
        _engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)
        async with _engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)
        await _engine.dispose()

    asyncio.run(setup())
    yield


@pytest.fixture(name='engine')
async def engine_fixture(settings):
    """engine"""
    _engine: AsyncEngine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )
    try:
        yield _engine
    finally:
        await _engine.dispose()


@pytest.fixture(name='session_factory')
async def session_factory_fixture(engine):
    """Session factory fixture"""
    yield sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(name='session')
async def session_fixture(migrate, session_factory) -> AsyncSession:
    """Session fixture."""
    async with session_factory() as _session:
        yield _session


@pytest.fixture(name='init_category')
async def init_category_fixture(session, settings):
    """init Category table data"""
    async with session.begin():
        categories = [
            CaptchaCategoryModel(
                name='test',
            )
        ]
        session.add_all(categories)


@pytest.fixture(name='init_record')
async def init_record_fixture(session, settings):
    """init Category table data"""
    async with session.begin():
        records = [
            CaptchaRecordModel(category_id=1, result='foo')
        ]
        session.add_all(records)


@pytest.fixture(name='init_storage')
async def init_storage_fixture(session, settings):
    """init_storage"""
    async with session.begin():
        storages = [
            StorageModel(
                name='local',
                uri='foo',
            )
        ]
        session.add_all(storages)


@pytest.fixture(name='init_file_record')
async def init_file_record_fixture(session, settings):
    """init_file_record"""
    async with session.begin():
        files = [
            CaptchaFileModel(
                record_id=1,
                filename='foo',
                file_type='foo',
                storage_id=1,
            ),
            CaptchaFileModel(
                record_id=1,
                filename='bar',
                file_type='foo',
                storage_id=1,
            ),
        ]
        session.add_all(files)


@pytest.fixture(name='client')
def app_client_fixture():
    """app_client_fixture"""
    client = TestClient(app)
    yield client
