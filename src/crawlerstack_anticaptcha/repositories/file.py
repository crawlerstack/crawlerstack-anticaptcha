"""CaptchaFileRepository"""
from sqlalchemy import select

from crawlerstack_anticaptcha.db import async_session
from crawlerstack_anticaptcha.models import CaptchaFileModel
from crawlerstack_anticaptcha.repositories.base import BaseRepository
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


class CaptchaFileRepository(BaseRepository):
    """CaptchaFileRepository"""

    @property
    def model(self):
        """model"""
        return CaptchaFileModel

    async def get_by_record_id(self, record_id: int):
        """get by record id"""
        stmt = select(self.model).where(self.model.record_id == record_id)
        async with async_session() as session:
            result = await session.scalars(stmt).all()
            if result is None:
                raise ObjectDoesNotExist('No captcha type found, Please upload correctly')
            self.logger.debug('Get %s from CaptchaFile', record_id)
            return result
