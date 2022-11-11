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
from crawlerstack_anticaptcha.storages import StorageFactory
from crawlerstack_anticaptcha.utils.exception import (CaptchaParseFailed,
                                                      UnsupportedMediaType)
from crawlerstack_anticaptcha.utils.schema import Message, MessageData


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
    storage = StorageFactory()

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
        category = await self.category_repository.get_by_name(self.category)
        if 'image' in self.image_type or 'image' in self.fore_image.content_type:

            if self.fore_image is None:
                file = await self.storage.factory(await self.image.read(), self.file_uuid,
                                                  PurePath(self.image.content_type).stem)
                parse_result = await self.parse(file.get('file'))
                if parse_result:
                    record = await self.record_repository.create_record(
                        CaptchaRecordModel(category_id=category.id, result=parse_result),
                        [CaptchaFileModel(filename=file.get('file'), file_type=self.image_type,
                                          storage_id=file.get('id'))]
                    )
                    result_message = Message(
                        code=200, data=MessageData(value=parse_result, category=self.category, id=record.id),
                        message='File parsing succeeded.'
                    )
                    return result_message

                await self.record_repository.create_record(
                    CaptchaRecordModel(category_id=category.id, result=parse_result, success=False),
                    [CaptchaFileModel(filename=file.get('file'), file_type=self.image_type, storage_id=file.get('id'))]
                )
                raise CaptchaParseFailed()

            if self.fore_image:
                raise CaptchaParseFailed(content='No other captcha features are currently available.')

        if 'image' not in self.image_type:
            raise UnsupportedMediaType(
                'The upload file format is incorrect, please upload the correct image type.'
            )

    async def parse(self, file: Path):
        """parse"""
        result = captcha_factory(self.category, file)
        if result:
            return result
        return False
