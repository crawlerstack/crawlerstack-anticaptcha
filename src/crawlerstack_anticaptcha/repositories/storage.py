"""StorageRepository"""
from fastapi_sa.database import db
from sqlalchemy.future import select

from crawlerstack_anticaptcha.db import StorageSchema
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

    @property
    def schema(self):
        """schema"""
        return StorageSchema

    async def init_default(self):
        """init default"""
        stmt = select(self.model).where(bool(self.model.default) is True)
        async with db():
            result = await db.session.scalars(stmt)
            for i in result.all():
                i.default = False
                await db.session.flush()

    async def get_by_name(self, storage_name: str):
        """get_by_name"""
        stmt = select(self.model).where(self.model.name == storage_name)
        res = await db.session.scalar(stmt)
        return self.schema.from_orm(res)

    async def update_by_name(self, name: str):
        """update_by_name"""
        stmt = select(self.model).where(self.model.name == name)
        async with db():
            obj = await db.session.scalar(stmt)
            if obj is None:
                raise ObjectDoesNotExist(f'Can not find object by id="{name}".')
            obj.default = True
            await db.session.flush()
            self.logger.info('Update %s', obj)
