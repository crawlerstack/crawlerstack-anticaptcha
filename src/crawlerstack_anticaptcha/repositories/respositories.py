"""SqlRepository"""
import logging

from sqlalchemy import delete
from sqlalchemy.engine import Result
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.repositories.models import (Base, CaptchaModel,
                                                          CategoryModel)

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_session = AsyncSession(engine, expire_on_commit=False)


class BaseRepository:
    """BaseRepository"""
    DATABASE_URL = settings.DATABASE_URL

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @property
    def model(self):
        """model"""
        raise NotImplementedError()

    async def create_all(self):
        """create_all"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            self.logger.info('Create all')

    async def drop_all(self):
        """drop_all"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            self.logger.info('Drop all')

    async def create(self, /, **kwargs):
        """
        insert
        :param kwargs:
        :return:
        """
        obj = self.model(**kwargs)
        try:
            async with async_session as session:
                session.add(obj)
                await session.commit()
                self.logger.info('Inserted %s', obj)
        except ProgrammingError:
            await self.create_all()
            async with async_session as session:
                session.add(obj)
                await session.commit()
                self.logger.info('Inserted %s', obj)

    async def get_by_id(self, pk):  # pylint:disable=C0103
        """
        get by id
        :param pk:
        :return:
        """
        stmt = select(self.model).where(self.model.id == pk)
        async with async_session as session:
            return await session.scalar(stmt)


class CategoryRepository(BaseRepository):
    """CategoryRepository"""

    @property
    def model(self):
        """model"""
        return CategoryModel

    async def add_all(self):
        """add all"""
        await self.create_all()
        async with async_session as session:
            session.add_all(
                [
                    CategoryModel(type='SliderCaptcha'),
                    CategoryModel(type='RotatedCaptcha')
                ]
            )
            await session.commit()


class CaptchaRepository(BaseRepository):
    """CaptchaRepository"""

    @property
    def model(self):
        """model"""
        return CaptchaModel

    async def query_all(self):
        """query_all"""
        self.logger.info('query all')
        async with async_session as session:
            result: Result = await session.execute(select(self.model))
            return result.scalars().all()

    async def get_by_file_id(self, file_id: str) -> CaptchaModel:
        """get_by_id"""
        self.logger.info('Get %s from Captcha', file_id)
        stmt = select(CaptchaModel).where(CaptchaModel.file_id == file_id)
        async with async_session as session:
            result = await session.scalar(stmt)
            return result

    @staticmethod
    async def delete_one(key):
        """delete one"""
        stmt = delete(CaptchaModel).where(CaptchaModel.file_id == key)
        async with async_session as session:
            await session.execute(stmt)
            await session.commit()

    async def update(self, file_id: str, success: bool):
        """update"""
        self.logger.info('Update file=%s success=%s', file_id, success)
        stmt = select(CaptchaModel).where(CaptchaModel.file_id == file_id)
        async with async_session as session:
            obj = await session.scalar(stmt)
            obj.success = success
            await session.commit()
