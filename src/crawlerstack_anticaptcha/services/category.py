"""category"""
from crawlerstack_anticaptcha.repositories.respositorie import \
    CategoryRepository
from crawlerstack_anticaptcha.utils.schema import Message


class CategoryService:
    """category service"""
    category_repository = CategoryRepository()

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
