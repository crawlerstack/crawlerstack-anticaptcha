"""test category repository"""
import logging

import pytest


@pytest.mark.asyncio
async def test_get_by_name(category_repository, init_category, caplog):
    """test get by name"""
    caplog.set_level(logging.DEBUG)
    result = await category_repository.get_by_name('test')
    assert 'Get' in caplog.text
    assert result.name == 'test'


@pytest.mark.asyncio
async def test_update_by_id(category_repository, caplog, init_category):
    """test_update_by_id"""
    caplog.set_level(logging.DEBUG)
    await category_repository.update_by_id(1, name='foo')
    assert 'Update' in caplog.text
    result = await category_repository.get_by_id(1)
    assert result.name == 'foo'
