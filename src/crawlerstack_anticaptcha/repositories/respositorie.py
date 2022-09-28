"""Repository"""
import logging

from sqlalchemy import delete
from sqlalchemy.future import select

from crawlerstack_anticaptcha.db import async_session
from crawlerstack_anticaptcha.models import CaptchaModel, CategoryModel
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
                self.logger.debug('Create %s', obj)

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
            return result


class CategoryRepository(BaseRepository):
    """CategoryRepository"""

    @property
    def model(self):
        """model"""
        return CategoryModel

    async def get_by_name(self, name: str) -> CategoryModel:
        """
        get by name
        :param name:
        :return:
        """
        stmt = select(self.model).where(self.model.name == name)
        async with async_session() as session:
            result = await session.scalar(stmt)
            if result is None:
                raise ObjectDoesNotExist('No captcha type found, Please upload correctly')
            self.logger.debug('Get %s from Captcha', name)
            return result


class CaptchaRepository(BaseRepository):
    """CaptchaRepository"""

    @property
    def model(self):
        """model"""
        return CaptchaModel

    async def get_by_file_id(self, file_id: str):
        """
        get by file id
        :param file_id:
        :return:
        """
        self.logger.debug('Get %s from "%s".', file_id, self.model.__tablename__)
        stmt = select(self.model).where(self.model.file_id == file_id)
        async with async_session() as session:
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
        async with async_session() as session:
            async with session.begin():
                obj = await session.scalar(stmt)
                if obj is None:
                    raise ObjectDoesNotExist(f'Can not find object by file_id="{file_id}".')
                obj.success = success
                self.logger.debug('Update %s.', obj)

    async def delete_by_file_id(self, file_id):
        """
        delete by file id
        :param file_id:
        :return:
        """
        stmt = delete(self.model).where(self.model.file_id == file_id)
        async with async_session() as session:
            async with session.begin():
                await session.execute(stmt)
