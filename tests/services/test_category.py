"""test category"""
import pytest

from crawlerstack_anticaptcha.services.category import CategoryService
from crawlerstack_anticaptcha.utils.schema import Message


@pytest.mark.asyncio
async def test_query_category(init_category):
    """test_query_category"""
    category = CategoryService()
    result = await category.get_all()
    assert result == Message(
        code=200,
        data=[
            {'id': 1, 'name': 'SliderCaptcha'},
            {'id': 2, 'name': 'RotatedCaptcha'},
            {'id': 3, 'name': 'NumericalCaptcha'}
        ],
        message='The identified captcha category can be provided.'
    )
