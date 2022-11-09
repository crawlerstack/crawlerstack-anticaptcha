"""test category repository"""
import datetime
import logging

import pytest

from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


@pytest.mark.asyncio
async def test_get_by_name(init_category, caplog):
    """test get by name"""
    category_repository = CategoryRepository()
    caplog.set_level(logging.DEBUG)
    result = await category_repository.get_by_name('test')
    assert 'Get' in caplog.text
    assert result.create_time == datetime.datetime(2022, 1, 1)

    with pytest.raises(ObjectDoesNotExist):
        await category_repository.get_by_name('foo')


@pytest.mark.asyncio
async def test_update_by_id(caplog, init_category):
    """test_update_by_id"""
    category_repository = CategoryRepository()
    caplog.set_level(logging.DEBUG)
    await category_repository.update_by_id(1, 'foo')
    assert 'Update' in caplog.text
    result = await category_repository.get_by_id(1)
    assert result.name == 'foo'
    assert result.create_time == datetime.datetime(2022, 1, 1)

    with pytest.raises(ObjectDoesNotExist):
        await category_repository.update_by_id(5, 'foo')
