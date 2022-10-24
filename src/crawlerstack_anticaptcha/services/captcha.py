"""Captcha Service"""
import logging
import uuid
from pathlib import Path, PurePath

from fastapi import File

from crawlerstack_anticaptcha.captcha import captcha_factory
from crawlerstack_anticaptcha.models import CategoryModel
from crawlerstack_anticaptcha.repositories.respositorie import (
    CaptchaRepository, CategoryRepository)
from crawlerstack_anticaptcha.utils.exception import (CaptchaParseFailed,
                                                      UnsupportedMediaType)
from crawlerstack_anticaptcha.utils.schema import Message, MessageData
from crawlerstack_anticaptcha.utils.upload_file import UploadedFile


class CaptchaService:
    """CaptchaService"""
    category_repository = CategoryRepository()
    captcha_repository = CaptchaRepository()

    def __init__(self, file: File, category: str, file_data: bytes):
        self.file = file
        self.category = category
        self.file_data = file_data
        self.file_uuid = str(uuid.uuid1())
        self.file_type = self.file.content_type
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def check(self) -> Message:
        """check"""
        captcha = await self.get_category()
        file = Path(captcha.path) / f'{self.file_uuid}.{PurePath(self.file_type).stem}'
        if 'image' in self.file_type:
            await self.save_file(file)
            parse_result = await self.parse(file, captcha.id)
            result_message = Message(
                code=200,
                data=MessageData(
                    value=parse_result,
                    category=captcha.name,
                    file_id=self.file_uuid
                ),
                message='File parsing succeeded.'
            )
            await self.write_to_db(
                file_id=self.file_uuid,
                category_id=captcha.id,
                file_type=PurePath(self.file_type).stem,
                success=None
            )
            return result_message

        if 'image' not in self.file_type:
            raise UnsupportedMediaType(
                'The upload file format is incorrect, please upload the correct image type.'
            )

    async def get_category(self) -> CategoryModel:
        """
        check category
        :return:
        """
        _category: CategoryModel = await self.category_repository.get_by_name(self.category)
        return _category

    async def write_to_db(self, **kwargs):
        """
        write to db
        :param kwargs:
        """
        await self.captcha_repository.create(**kwargs)

    async def save_file(self, file: Path):
        """save file"""
        upload_file = UploadedFile(self.file_data, file)
        await upload_file.save()

    async def parse(self, file: Path, captcha_id: int):
        """parse"""
        captcha_service = captcha_factory(self.category, file)
        result = captcha_service.parse()
        if result:
            return result
        await self.captcha_repository.create(
            file_id=self.file_uuid, category_id=captcha_id,
            file_type=PurePath(self.file_type).stem,
            success=False
        )
        raise CaptchaParseFailed()
