"""StorageRepository"""

from sqlalchemy.future import select

from crawlerstack_anticaptcha.db import async_session
from crawlerstack_anticaptcha.models import StorageModel
from crawlerstack_anticaptcha.repositories.base import BaseRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


class StorageRepository(BaseRepository):
    """
    StorageRepository
    """

    @property
    def model(self):
        """model"""
        return StorageModel

    async def update_by_id(self, storage_id: int, default: bool):
        """
        update_by_id
        :param storage_id:
        :param default:
        :return:
        """
        stmt = select(self.model).where(self.model.id == storage_id)
        async with async_session() as session:
            async with session.begin():
                obj = await session.scalar(stmt)
                if obj is None:
                    raise ObjectDoesNotExist(f'Can not find object by id="{storage_id}".')
                obj.default = default
                self.logger.info('Update %s', obj)

    async def init_default(self):
        """init default"""
        stmt = select(self.model).where(bool(self.model.default) is True)
        async with async_session() as session:
            async with session.begin():
                result = await session.scalars(stmt)
                for i in result.all():
                    i.default = False

    async def get_by_name(self, storage_name: str):
        """get_by_name"""
        stmt = select(self.model).where(self.model.name == storage_name)
        async with async_session() as session:
            res = await session.scalar(stmt)
            return res

    async def update_by_name(self, name: str):
        """update_by_name"""
        stmt = select(self.model).where(self.model.name == name)
        async with async_session() as session:
            async with session.begin():
                obj = await session.scalar(stmt)
                if obj is None:
                    raise ObjectDoesNotExist(f'Can not find object by id="{name}".')
                obj.default = True
                self.logger.info('Update %s', obj)
