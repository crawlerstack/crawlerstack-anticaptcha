"""Test config"""
import asyncio
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from crawlerstack_anticaptcha import config
from crawlerstack_anticaptcha.db import BaseModel
from crawlerstack_anticaptcha.models import CaptchaModel, CategoryModel


@pytest.fixture(name='settings')
def settings_fixture():
    """settings fixture"""
    return config.settings


@pytest.fixture
def mock_path() -> Path:
    """Mock a path, and clean when unit test done."""
    with TemporaryDirectory() as temp_path:
        yield Path(temp_path)


@pytest.fixture(autouse=True, name='migrate')
def migrate_fixture(settings):
    """migrate fixture"""

    async def setup():
        """setup"""
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
                path=str(Path(f'{settings.IMAGE_SAVE_PATH}').joinpath(Path('slider-captcha')))
            ),
            CategoryModel(
                name='RotatedCaptcha',
                path=str(Path(f'{settings.IMAGE_SAVE_PATH}').joinpath(Path('rotated-captcha')))
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
                creation_time=datetime.today(),
            ),
        ]
        session.add_all(captchas)
