"""Captcha Service"""
import logging
import uuid
from datetime import datetime
from pathlib import Path, PurePath

from fastapi import File

from crawlerstack_anticaptcha.captcha import captcha_factory
from crawlerstack_anticaptcha.models import StorageModel
from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.repositories.file import CaptchaFileRepository
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.utils.exception import (CaptchaParseFailed,
                                                      UnsupportedMediaType)
from crawlerstack_anticaptcha.utils.schema import (Captcha, CaptchaPath,
                                                   Message, MessageData)
from crawlerstack_anticaptcha.utils.upload_file import UploadedFile


async def save(file_data: bytes, file: Path):
    """save image"""
    upload_file = UploadedFile(file_data, file)
    await upload_file.save()


async def storage_default() -> StorageModel:
    """获取存储配置"""
    storage = StorageRepository()
    default = await storage.get_default()
    return default


class CaptchaService:
    """CaptchaService"""
    category_repository = CategoryRepository()
    record_repository = CaptchaRecordRepository()
    file_repository = CaptchaFileRepository()

    def __init__(self, image: File, category: str, fore_image: File = None, extra_content: str = None):
        self.image: File() = image
        self.extra_content = extra_content
        self.image_type = image.content_type
        self.fore_image: File() = fore_image
        self.category = category
        self.file_uuid = str(uuid.uuid1())
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def check(self) -> Message:
        """check"""
        storage: StorageModel = await storage_default()
        category = await self.category_repository.get_by_name(self.category)
        if 'image' in self.image_type or 'image' in self.fore_image.content_type:

            if self.fore_image is None:
                file = await self.check_category(storage.uri, self.image)
                file_data = await self.image.read()
                await save(file_data, file)
                parse_result = await self.parse(file)
                if parse_result:
                    record_id = await self.write_to_db(
                        category_id=category.id, file_type=PurePath(self.image_type).stem,
                        success=None, result=parse_result, filename=self.file_uuid,
                        storage_id=storage.id
                    )
                    result_message = Message(
                        code=200, data=MessageData(value=parse_result, category=self.category, id=record_id),
                        message='File parsing succeeded.'
                    )
                    return result_message
                await self.write_to_db(
                    category_id=category.id, file_type=PurePath(self.image_type).stem,
                    success=False, result=None, filename=self.file_uuid,
                    storage_id=storage.id
                )
                raise CaptchaParseFailed()

            if self.fore_image:
                raise CaptchaParseFailed(content='No other captcha features are currently available.')

        if 'image' not in self.image_type:
            raise UnsupportedMediaType(
                'The upload file format is incorrect, please upload the correct image type.'
            )

    async def check_category(self, path: str, file: File()) -> Path:
        """check category"""
        if self.category == Captcha.Slider.value:
            return Path(path) / CaptchaPath.Slider.value / f'{self.file_uuid}.{PurePath(file.content_type).stem}'
        if self.category == Captcha.Numerical.value:
            return Path(path) / CaptchaPath.Numerical.value / f'{self.file_uuid}.{PurePath(file.content_type).stem}'

    async def write_to_db(
            self,
            category_id: int,
            file_type: str,
            success: bool | None,
            result,
            filename: str,
            storage_id: int,
    ):
        """
        write to db
        """
        record_id = await self.record_repository.create_record(
            category_id=category_id, result=result, success=success, update_time=None, create_time=datetime.now()
        )
        await self.file_repository.create(
            record_id=record_id, filename=filename, file_type=file_type, storage_id=storage_id, update_time=None,
            create_time=datetime.now()
        )
        return record_id

    async def parse(self, file: Path):
        """parse"""
        captcha_service = captcha_factory(self.category, file)
        result = captcha_service.parse()
        if result:
            return result
        return False
