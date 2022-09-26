"""SqlRepository"""
import logging
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.repositories.models import (Base, CaptchaModel,
                                                          CategoryModel)
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_session = AsyncSession(engine, expire_on_commit=False)


class BaseRepository:
    """BaseRepository"""
    DATABASE_URL = settings.DATABASE_URL
    PK_TABLE = 'category'

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @property
    def model(self):
        """model"""
        raise NotImplementedError()

    async def table_exists(self):
        """table_exists"""
        async with async_session as session:
            result = await session.execute(select(self.model))
            return result

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

    async def query_all(self):
        """query_all"""
        self.logger.info('query all')
        async with async_session as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def get_by_id(self, pk: int):
        """
        get by id
        :param pk:
        :return:
        """
        stmt = select(self.model).where(self.model.id == pk)
        async with async_session as session:
            result = await session.scalar(stmt)
            return result


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
                    CategoryModel(
                        name='SliderCaptcha',
                        path=str(Path(f'{settings.IMAGE_SAVE_PATH}').joinpath(Path('slider-captcha')))
                    ),
                    CategoryModel(
                        name='RotatedCaptcha',
                        path=str(Path(f'{settings.IMAGE_SAVE_PATH}').joinpath(Path('rotated-captcha')))
                    )
                ])
            await session.commit()

    async def get_by_name(self, name: str) -> CategoryModel:
        """
        get by name
        :param name:
        :return:
        """
        stmt = select(self.model).where(self.model.name == name)
        async with async_session as session:
            result = await session.scalar(stmt)
            if result is None:
                self.logger.info('Object Does Not Exist')
                raise ObjectDoesNotExist('No captcha type found')
            self.logger.info('Get %s from Captcha', name)
            return result


class CaptchaRepository(BaseRepository):
    """CaptchaRepository"""

    @property
    def model(self):
        """model"""
        return CaptchaModel

    async def get_by_file_id(self, file_id: str):
        """get_by_file_id"""
        self.logger.info('Get %s from Captcha', file_id)
        stmt = select(self.model).where(self.model.file_id == file_id)
        async with async_session as session:
            result = await session.scalar(stmt)
            return result

    async def update_by_file_id(self, file_id: str, success: bool):
        """
        update by file id
        :param file_id:
        :param success:
        :return:
        """
        stmt = select(self.model).where(self.model.file_id == file_id)
        async with async_session as session:
            obj = await session.scalar(stmt)
            if obj is None:
                raise ObjectDoesNotExist('File Id Does Not Exist')
            obj.success = success
            await session.commit()
            self.logger.info('Update file=%s success=%s', file_id, success)

    async def delete_by_file_id(self, file_id):
        """
        delete one
        :param file_id:
        :return:
        """
        stmt = delete(self.model).where(self.model.file_id == file_id)
        async with async_session as session:
            await session.execute(stmt)
            await session.commit()
