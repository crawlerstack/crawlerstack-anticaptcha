"""Test Repository"""

import pytest

from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


@pytest.mark.asyncio
async def test_get_by_name(category_repository, init_category):
    """test_table_exists"""
    result = await category_repository.get_by_name('SliderCaptcha')
    assert result.id == 1


@pytest.mark.asyncio
async def test_get_by_id(category_repository, init_category):
    """test_get_by_id"""
    result = await category_repository.get_by_id(1)
    assert result.name == 'SliderCaptcha'


@pytest.mark.asyncio
async def test_create(captcha_repository, init_category):
    """test_captcha_insert"""
    await captcha_repository.create(
        file_id='test',
        success=None
    )
    result = await captcha_repository.get_by_file_id('test')
    assert result.success is None


@pytest.mark.asyncio
async def test_captcha_update(captcha_repository, init_category):
    """test_captcha_update"""
    await captcha_repository.create(
        file_id='test',
    )
    await captcha_repository.update_by_file_id('test', False)
    result = await captcha_repository.get_by_file_id('test')
    assert not result.success


@pytest.mark.asyncio
async def test_query_all(captcha_repository, init_captcha):
    """test_query_all"""
    result = await captcha_repository.get_all()
    for _i in result:
        assert _i.file_id == 'foo'
        assert _i.success is None


@pytest.mark.asyncio
async def test_delete_by_file_id(captcha_repository, init_captcha):
    """test_delete_by_file_id"""
    await captcha_repository.delete_by_file_id('foo')
    result = await captcha_repository.get_by_file_id('foo')
    assert not result


@pytest.mark.parametrize(
    'key',
    [
        True,
        False
    ]
)
@pytest.mark.asyncio
async def test_update_by_file_id(captcha_repository, init_captcha, key):
    """test_update_by_file_id"""
    if key:
        await captcha_repository.update_by_file_id('foo', True)
        res = await captcha_repository.get_by_file_id('foo')
        assert res.success
    with pytest.raises(ObjectDoesNotExist):
        await captcha_repository.update_by_file_id('bar', True)
