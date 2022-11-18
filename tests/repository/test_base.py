"""Test Repository"""

import pytest
from sqlalchemy import func, select

from crawlerstack_anticaptcha.models import CaptchaCategoryModel
from crawlerstack_anticaptcha.repositories.base import BaseRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist
from crawlerstack_anticaptcha.utils.schema import CaptchaCategorySchema


def test_model():
    """test model"""
    base = BaseRepository()
    with pytest.raises(NotImplementedError):
        base.model()


def test_schema():
    """test model"""
    base = BaseRepository()
    with pytest.raises(NotImplementedError):
        base.schema()


@pytest.mark.asyncio
async def test_create(session, category_repository):
    """test_captcha_insert"""
    obj = await category_repository.create(name='foo')
    res = await session.scalar(select(func.count()).select_from(CaptchaCategoryModel))
    assert res == 1
    assert obj == CaptchaCategorySchema(id=1, name='foo')


@pytest.mark.asyncio
async def test_get_all(session, category_repository, init_category):
    """test_get_all"""
    result = await category_repository.get_all()
    length = await session.scalar(select(func.count()).select_from(CaptchaCategoryModel))
    assert len(result) == length


@pytest.mark.asyncio
async def test_get_by_id(session, category_repository, init_category):
    """test_get_by_id"""
    result = await category_repository.get_by_id(1)
    assert result.name == 'test'

    with pytest.raises(ObjectDoesNotExist):
        await category_repository.get_by_id(5)


@pytest.mark.asyncio
async def test_delete_by_id(session, category_repository, init_category):
    """test_table_exists"""
    await category_repository.delete_by_id(1)
    with pytest.raises(ObjectDoesNotExist):
        await category_repository.get_by_id(1)


@pytest.mark.asyncio
async def test_update_by_id(session, category_repository, init_category):
    """test update by id"""
    await category_repository.update_by_id(1, name='foo')
    res = await category_repository.get_by_id(1)
    assert res.name == 'foo'
