"""Repository"""
import logging

from sqlalchemy import delete
from sqlalchemy.future import select

from crawlerstack_anticaptcha.db import async_session
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist


class BaseRepository:
    """BaseRepository"""

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @property
    def model(self):
        """model"""
        raise NotImplementedError()

    async def create(self, /, **kwargs):
        """
        create
        :param kwargs:
        :return:
        """
        obj = self.model(**kwargs)
        async with async_session() as session:
            async with session.begin():
                session.add(obj)
                self.logger.info('Create %s', obj)
        return obj

    async def get_all(self):
        """get all"""
        async with async_session() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def get_by_id(self, pk: int):
        """
        get by id
        :param pk:
        :return:
        """
        stmt = select(self.model).where(self.model.id == pk)
        async with async_session() as session:
            result = await session.scalar(stmt)
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
        async with async_session() as session:
            async with session.begin():
                await session.execute(stmt)
