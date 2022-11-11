"""CaptchaRecordRepository"""
from typing import List

from sqlalchemy.future import select

from crawlerstack_anticaptcha.db import async_session
from crawlerstack_anticaptcha.models import (CaptchaFileModel,
                                             CaptchaRecordModel)
from crawlerstack_anticaptcha.repositories.base import BaseRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


class CaptchaRecordRepository(BaseRepository):
    """CaptchaRecordRepository"""

    @property
    def model(self):
        """model"""
        return CaptchaRecordModel

    async def create_record(self, record_obj: CaptchaRecordModel, file_objs: List[CaptchaFileModel]):
        """
        create_record
        """
        async with async_session() as session:
            async with session.begin():
                session.add(record_obj)
                await session.flush()
                for file_obj in file_objs:
                    file_obj.record_id = record_obj.id
                    session.add(file_obj)
        self.logger.debug('Create %s', record_obj)
        return record_obj

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
                obj.success = success
                self.logger.debug('Update %s.', obj)
