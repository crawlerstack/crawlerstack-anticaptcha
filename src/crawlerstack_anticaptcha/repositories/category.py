"""CategoryRepository"""
from datetime import datetime

from sqlalchemy.future import select

from crawlerstack_anticaptcha.db import async_session
from crawlerstack_anticaptcha.models import CaptchaCategoryModel
from crawlerstack_anticaptcha.repositories.base import BaseRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


class CategoryRepository(BaseRepository):
    """CategoryRepository"""

    @property
    def model(self):
        """model"""
        return CaptchaCategoryModel

    async def get_by_name(self, name: str) -> CaptchaCategoryModel:
        """
        通过类型名称查找对应的id

        :param name:
        :return:
        """
        stmt = select(self.model).where(self.model.name == name)
        async with async_session() as session:
            result = await session.scalar(stmt)
            if result is None:
                raise ObjectDoesNotExist('No captcha type found, Please upload correctly')
            self.logger.debug('Get %s from Captcha', name)
            return result

    async def update_by_id(self, pk: int, name: str):
        """
        update by id
        :param pk:
        :param name:
        :return:
        """
        stmt = select(self.model).where(self.model.id == pk)
        async with async_session() as session:
            async with session.begin():
                obj = await session.scalar(stmt)
                if obj is None:  # pylint: disable=duplicate-code
                    raise ObjectDoesNotExist(f'Can not find object by id="{pk}"')
                obj.name = name
                obj.update_time = datetime.now()
                self.logger.debug('Update %s', obj)
