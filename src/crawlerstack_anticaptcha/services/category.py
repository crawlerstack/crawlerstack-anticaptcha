"""category"""
from datetime import datetime

from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.utils.schema import Message


class CategoryService:
    """category service"""
    category_repository = CategoryRepository()

    def __init__(self, category_id: int = None, name: str = None):
        self.name = name
        self.category_id = category_id
        self.now = datetime.now()

    async def get_all(self):
        """query_category"""
        category_list = []
        for i in await self.category_repository.get_all():
            category_list.append({'id': i.id, 'name': i.name})
        return Message(
            code=200,
            data=category_list,
            message='The identified captcha category can be provided.'
        )

    async def create(self):
        """create"""
        await self.category_repository.create(
            name=self.name,
        )
        return Message(
            code=200,
            message='ok'
        )

    async def update(self):
        """update"""
        await self.category_repository.update_by_id(self.category_id, self.name)
        return Message(
            code=200,
            message='ok'
        )
