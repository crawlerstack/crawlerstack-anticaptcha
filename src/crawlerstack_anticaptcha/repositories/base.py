"""Repository"""
import logging

from fastapi_sa.database import db, session_ctx
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

    @session_ctx
    async def create(self, /, **kwargs):
        """
        create
        :param kwargs:
        :return:
        """
        obj = self.model(**kwargs)
        async with db() as session:
            session.add(obj)
            self.logger.info('Create %s', obj)
        return obj

    async def get_all(self):
        """get all"""
        result = await db.session.execute(select(self.model))
        return result.scalars().all()

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
        return result

    async def delete_by_id(self, pk: int):
        """
        delete by id
        :param pk:
        :return:
        """
        stmt = delete(self.model).where(self.model.id == pk)
        async with db() as session:
            await session.execute(stmt)

    async def update_by_id(self, pk: int, **kwargs):
        """update by id"""
        obj = await db.session.get(self.model, pk)
        for k, v in kwargs.items():
            setattr(obj, k, v)
        db.session.flush()
        self.logger.debug('Update %s', obj)
        return obj
