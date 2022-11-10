"""Captcha Service"""
import logging
import uuid
from pathlib import Path, PurePath

from fastapi import File

from crawlerstack_anticaptcha.captcha import captcha_factory
from crawlerstack_anticaptcha.models import (CaptchaFileModel,
                                             CaptchaRecordModel, StorageModel)
from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.repositories.file import CaptchaFileRepository
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.utils.exception import (CaptchaParseFailed,
                                                      UnsupportedMediaType)
from crawlerstack_anticaptcha.utils.schema import Captcha, Message, MessageData
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
                file = Path(storage.uri) / f'{self.file_uuid}.{PurePath(self.image.content_type).stem}'
                file_data = await self.image.read()
                await save(file_data, file)
                parse_result = await self.parse(file)
                if parse_result:
                    record = await self.record_repository.create_record(
                        CaptchaRecordModel(category_id=category.id, result=parse_result),
                        [CaptchaFileModel(filename=file, file_type=self.image_type, storage_id=storage.id)]
                    )
                    result_message = Message(
                        code=200, data=MessageData(value=parse_result, category=self.category, id=record.id),
                        message='File parsing succeeded.'
                    )
                    return result_message

                await self.record_repository.create_record(
                    CaptchaRecordModel(category_id=category.id, result=parse_result, success=False),
                    [CaptchaFileModel(filename=file, file_type=self.image_type, storage_id=storage.id)]
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
            return Path(path) / f'{self.file_uuid}.{PurePath(file.content_type).stem}'
        if self.category == Captcha.Numerical.value:
            return Path(path) / f'{self.file_uuid}.{PurePath(file.content_type).stem}'

    async def parse(self, file: Path):
        """parse"""
        captcha_service = captcha_factory(self.category, file)
        result = captcha_service.parse()
        if result:
            return result
        return False
