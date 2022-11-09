"""StorageRepository"""
from datetime import datetime

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
                obj.update_time = datetime.now()
                self.logger.info('Update %s', obj)

    async def get_default(self):
        """get default"""
        stmt = select(self.model).where(bool(self.model.default) is True)
        async with async_session() as session:
            result = await session.scalar(stmt)
            if result is None:
                raise ObjectDoesNotExist('No default configuration found available')
            return result
