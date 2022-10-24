"""Test config"""
import asyncio
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from crawlerstack_anticaptcha import config
from crawlerstack_anticaptcha.api import app
from crawlerstack_anticaptcha.models import (BaseModel, CaptchaModel,
                                             CategoryModel)
from crawlerstack_anticaptcha.repositories.respositorie import (
    CaptchaRepository, CategoryRepository)


@pytest.fixture(name='settings')
def settings_fixture():
    """settings fixture"""
    return config.settings


@pytest.fixture
def mock_path() -> Path:
    """Mock a path, and clean when unit test done."""
    with TemporaryDirectory() as temp_path:
        yield Path(temp_path)


@pytest.fixture(name='category_repository')
def category_repository_fixture():
    """category repository fixture"""
    category_repository = CategoryRepository()
    yield category_repository


@pytest.fixture(name='captcha_repository')
def captcha_repository_fixture():
    """captcha repository fixture"""
    captcha_repository = CaptchaRepository()
    yield captcha_repository


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
            CategoryModel(
                name='SliderCaptcha',
                path=str(Path(settings.CAPTCHA_IMAGE_PATH) / 'slider_captcha')
            ),
            CategoryModel(
                name='RotatedCaptcha',
                path=str(Path(settings.CAPTCHA_IMAGE_PATH) / 'rotated_captcha')
            ),
            CategoryModel(
                name='NumericalCaptcha',
                path=str(Path(settings.CAPTCHA_IMAGE_PATH) / 'numerical_captcha')
            )
        ]
        session.add_all(categories)


@pytest.fixture(name='init_captcha')
async def init_captcha_fixture(session, init_category):
    """init captcha table data"""
    async with session.begin():
        result = await session.scalars(select(CategoryModel))
        objs = result.all()
        captchas = [
            CaptchaModel(
                file_id='foo',
                category_id=objs[0].id,
            ),
        ]
        session.add_all(captchas)


@pytest.fixture(name='client')
def app_client_fixture():
    """app_client_fixture"""
    client = TestClient(app)
    yield client
