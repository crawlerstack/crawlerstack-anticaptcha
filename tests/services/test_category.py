"""test category"""

import pytest

from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.services.category import CategoryService
from crawlerstack_anticaptcha.utils.schema import Message


@pytest.mark.asyncio
async def test_get_all(init_category):
    """test_get_all"""
    category = CategoryService()
    result = await category.get_all()
    assert result == Message(code=200, data=[], message='The identified captcha category can be provided.')


@pytest.mark.asyncio
async def test_create(mocker):
    """test create"""
    category = CategoryService(category_id=1, name='foo')
    create = mocker.patch.object(CategoryRepository, 'create')
    result = await category.create()
    create.assert_called()
    assert result == Message(code=200, data=None, message='ok')


@pytest.mark.asyncio
async def test_update(mocker):
    """test update"""
    category = CategoryService(category_id=1, name='foo')
    update_by_id = mocker.patch.object(CategoryRepository, 'update_by_id')
    result = await category.update()
    update_by_id.assert_called_with(1, name='foo')
    assert result == Message(code=200, data=None, message='ok')
