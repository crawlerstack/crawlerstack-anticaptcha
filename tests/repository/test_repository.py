"""Test Repository"""
import datetime

import pytest

from crawlerstack_anticaptcha.repositories.respositories import (
    CaptchaRepository, CategoryRepository)

category_repository = CategoryRepository()
captcha_repository = CaptchaRepository()


@pytest.mark.asyncio
async def test_get_by_name(init_category):
    """test_table_exists"""
    result = await category_repository.get_by_name('SliderCaptcha')
    assert result.id == 1


@pytest.mark.asyncio
async def test_get_by_id(init_category):
    """test_get_by_id"""
    result = await category_repository.get_by_id(1)
    assert result.name == 'SliderCaptcha'


@pytest.mark.asyncio
async def test_create(init_category):
    """test_captcha_insert"""
    await captcha_repository.create(
        file_id='test',
        creation_time=datetime.datetime.today(),
        success=None
    )
    result = await captcha_repository.get_by_file_id('test')
    assert result.success is None


@pytest.mark.asyncio
async def test_captcha_update(init_category):
    """test_captcha_update"""
    await captcha_repository.create(
        file_id='test',
        creation_time=datetime.datetime.today(),
    )
    await captcha_repository.update_by_file_id('test', False)
    result = await captcha_repository.get_by_file_id('test')
    assert not result.success


@pytest.mark.asyncio
async def test_query_all(init_captcha):
    """test_query_all"""
    result = await captcha_repository.query_all()
    for _i in result:
        assert _i.file_id == 'foo'
        assert _i.success is None


@pytest.mark.asyncio
async def test_delete_by_file_id(init_captcha):
    """test_delete_by_file_id"""
    await captcha_repository.delete_by_file_id('foo')
    result = await captcha_repository.get_by_file_id('foo')
    assert result is None
