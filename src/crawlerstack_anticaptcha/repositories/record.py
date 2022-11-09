"""CaptchaRecordRepository"""

from datetime import datetime

from sqlalchemy.future import select

from crawlerstack_anticaptcha.db import async_session
from crawlerstack_anticaptcha.models import CaptchaRecordModel
from crawlerstack_anticaptcha.repositories.base import BaseRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


class CaptchaRecordRepository(BaseRepository):
    """CaptchaRecordRepository"""

    @property
    def model(self):
        """model"""
        return CaptchaRecordModel

    async def create_record(self, **kwargs):
        """
        create_record
        :param kwargs:
        :return:
        """
        obj = CaptchaRecordModel(**kwargs)
        async with async_session() as session:
            async with session.begin():
                session.add(obj)
                self.logger.debug('Create %s', obj)
        return obj.id

    async def update_by_pk(self, pk: int, success: bool):
        """
        update by file id
        :param pk:
        :param success:
        :return:
        """
        stmt = select(self.model).where(self.model.id == pk)
        async with async_session() as session:
            async with session.begin():
                obj = await session.scalar(stmt)
                if obj is None:
                    raise ObjectDoesNotExist(f'Can not find object by id="{pk}".')
                obj.update_time = datetime.now()
                obj.success = success
                self.logger.debug('Update %s.', obj)
