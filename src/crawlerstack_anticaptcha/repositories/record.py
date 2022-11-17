"""CaptchaRecordRepository"""
from typing import List

from fastapi_sa.database import db

from crawlerstack_anticaptcha.models import (CaptchaFileModel,
                                             CaptchaRecordModel)
from crawlerstack_anticaptcha.repositories.base import BaseRepository


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
        session = db.session
        session.add(record_obj)
        await session.flush()
        for file_obj in file_objs:
            file_obj.record_id = record_obj.id
            session.add(file_obj)
        self.logger.debug('Create %s', record_obj)
        return record_obj
