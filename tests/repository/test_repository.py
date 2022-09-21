"""Test Repository"""

import pytest

from crawlerstack_anticaptcha.repositories.respositories import (
    CaptchaRepository, CategoryRepository)

category_repository = CategoryRepository()
captcha_repository = CaptchaRepository()


@pytest.mark.asyncio
async def test_get_by_id():
    """test_get_by_id"""
    await category_repository.drop_all()
    await category_repository.add_all()
    result = await category_repository.get_by_id(1)
    assert result.type == 'SliderCaptcha'

# @pytest.mark.asyncio
# async def test_create():
#     """test_captcha_insert"""
#     await category_repository.drop_all()
#     await category_repository.create(type='foo')
#     await captcha_repository.create(
#         file_id='test',
#         category_id=1,
#         file_path='foo',
#         file_type='foo',
#         creation_time=datetime.datetime.today(),
#         success=None
#     )
#     result = await captcha_repository.get_by_file_id('test')
#     assert result.file_type == 'foo'

# @pytest.mark.asyncio
# async def test_captcha_update():
#     """test_captcha_update"""
#     loop = asyncio.get_event_loop()
#     await category_repository.add_all()
#     await captcha_repository.create(
#         file_id='test',
#         creation_time=datetime.datetime.today(),
#     )
#     await captcha_repository.update('test', False)
#     result = await captcha_repository.get_by_file_id('test')
#     assert not result.success
#     loop.close()
