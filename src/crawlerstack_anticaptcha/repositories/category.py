"""CategoryRepository"""
from fastapi_sa.database import db
from sqlalchemy.future import select

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
        result = await db.session.scalar(stmt)
        if result is None:
            raise ObjectDoesNotExist('No captcha type found, Please upload correctly')
        self.logger.debug('Get %s from Captcha', name)
        return result
