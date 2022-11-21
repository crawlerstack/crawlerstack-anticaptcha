"""Repository"""
import logging

from fastapi_sa.database import db
from sqlalchemy import delete
from sqlalchemy.future import select

from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


class BaseRepository:
    """BaseRepository"""

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @property
    def model(self):
        """model"""
        raise NotImplementedError()

    @property
    def schema(self):
        """Schema"""
        raise NotImplementedError()

    async def create(self, /, **kwargs):
        """
        create
        :param kwargs:
        :return:
        """
        obj = self.model(**kwargs)
        db.session.add(obj)
        await db.session.flush()
        self.logger.info('Create %s', obj)
        return self.schema.from_orm(obj)

    async def get_all(self):
        """get all"""
        result = await db.session.scalars(select(self.model))
        objs = [self.schema.from_orm(i) for i in result.all()]
        return objs

    async def get_by_id(self, pk: int):
        """
        get by id
        :param pk:
        :return:
        """
        stmt = select(self.model).where(self.model.id == pk)
        result = await db.session.scalar(stmt)
        if result is None:
            raise ObjectDoesNotExist(f'Can not find object by id="{pk}".')
        return self.schema.from_orm(result)

    async def delete_by_id(self, pk: int):
        """
        delete by id
        :param pk:
        :return:
        """
        stmt = delete(self.model).where(self.model.id == pk)
        await db.session.execute(stmt)

    async def update_by_id(self, pk: int, **kwargs):
        """update by id"""
        obj = await db.session.get(self.model, pk)
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await db.session.flush()
        self.logger.debug('Update %s', obj)
        return self.schema.from_orm(obj)
