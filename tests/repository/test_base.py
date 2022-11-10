"""Test Repository"""

import pytest

from crawlerstack_anticaptcha.repositories.base import BaseRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


def test_model():
    """test model"""
    base = BaseRepository()
    with pytest.raises(NotImplementedError):
        base.model()


@pytest.mark.asyncio
async def test_delete_by_id(category_repository, init_category):
    """test_table_exists"""
    await category_repository.delete_by_id(1)
    with pytest.raises(ObjectDoesNotExist):
        await category_repository.get_by_id(1)


@pytest.mark.asyncio
async def test_get_by_id(category_repository, init_category):
    """test_get_by_id"""
    result = await category_repository.get_by_id(1)
    assert result.name == 'test'

    with pytest.raises(ObjectDoesNotExist):
        await category_repository.get_by_id(5)


@pytest.mark.asyncio
async def test_create(category_repository):
    """test_captcha_insert"""
    await category_repository.create(
        name='foo',
    )
    result = await category_repository.get_by_id(1)
    assert result.name == 'foo'


@pytest.mark.asyncio
async def test_get_all(category_repository, init_category):
    """test_get_all"""
    result = await category_repository.get_all()
    for _i in result:
        assert _i.name == 'test'
