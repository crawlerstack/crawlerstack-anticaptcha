"""Captcha Service"""
import logging
import uuid
from pathlib import PurePath
from typing import List

from fastapi import File

from crawlerstack_anticaptcha.captcha import CaptchaParser
from crawlerstack_anticaptcha.models import (CaptchaCategoryModel,
                                             CaptchaFileModel,
                                             CaptchaRecordModel)
from crawlerstack_anticaptcha.repositories.category import CategoryRepository
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.storages import Storage
from crawlerstack_anticaptcha.utils.exception import (CaptchaParseFailed,
                                                      UnsupportedMediaType)
from crawlerstack_anticaptcha.utils.message import Message, MessageData


class CaptchaService:
    """CaptchaService"""
    category_repository = CategoryRepository()
    record_repository = CaptchaRecordRepository()
    storage = Storage()

    def __init__(self, bg_image: File, category: str, fore_image: File = None, extra_content: str = None):
        self.bg_image: File() = bg_image
        self.extra_content = extra_content
        self.fore_image: File() = fore_image
        self.category = category
        self.captcha = CaptchaParser(category)
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def check(self) -> Message:
        """check"""
        category = await self.category_repository.get_by_name(self.category)
        if 'image' in self.bg_image.content_type or 'image' in self.fore_image.content_type:

            if self.fore_image is None:
                file_uuid = str(uuid.uuid1())
                file_info = await self.save_file(file_uuid)
                parse_result = await self.parse(file_info[0])
                if parse_result:
                    record = await self.image_record(category, parse_result, file_info)
                    result_message = Message(
                        code=200, data=MessageData(value=parse_result, category=self.category, id=record.id),
                        message='File parsing succeeded.'
                    )
                    return result_message
                await self.image_record(category, parse_result, file_info, success=False)
                raise CaptchaParseFailed()

            if self.fore_image:
                bg_img_file_uuid = str(uuid.uuid1())
                fore_img_file_uuid = str(uuid.uuid1())
                file_info = await self.save_file(bg_img_file_uuid, fore_img_file_uuid)
                parse_result = await self.parse(file_info[0], file_info[1])
                if parse_result:
                    record = await self.image_record(
                        category, parse_result, file_info
                    )
                    result_message = Message(
                        code=200, data=MessageData(value=parse_result, category=self.category, id=record.id),
                        message='File parsing succeeded.'
                    )
                    return result_message

                await self.image_record(
                    category, parse_result, file_info, success=False
                )
                raise CaptchaParseFailed()

        else:
            raise UnsupportedMediaType(
                'The upload file format is incorrect, please upload the correct image type.'
            )

    async def parse(self, background_file: dict, fore_file: dict = None):
        """parse"""
        if fore_file:
            return self.captcha.factory(background_file.get('file'), fore_file.get('file'), self.extra_content)
        return self.captcha.factory(background_file.get('file'), fore_file, self.extra_content)

    async def save_file(self, bg_img_file_uuid: str, fore_img_file_uuid: str = None):
        """save file"""
        bg_data = await self.bg_image.read()
        if fore_img_file_uuid:
            fore_data = await self.fore_image.read()
            bg_img_file: dict = await self.storage.factory(
                bg_data, bg_img_file_uuid, PurePath(self.bg_image.content_type).stem
            )
            fore_img_file: dict = await self.storage.factory(
                fore_data, fore_img_file_uuid, PurePath(self.fore_image.content_type).stem
            )
            return [bg_img_file, fore_img_file]
        return [await self.storage.factory(bg_data, bg_img_file_uuid, PurePath(self.bg_image.content_type).stem)]

    async def image_record(
            self,
            category: CaptchaCategoryModel,
            parse_result: str | int,
            file_info: List[dict],
            success: bool = None
    ):
        """image_record"""
        captcha_files = []
        for i in file_info:
            captcha_files.append(
                CaptchaFileModel(
                    filename=i.get('file_name'),
                    file_type=i.get('file_type'),
                    storage_id=i.get('id'),
                    file_mark='Background image',
                )
            )

        record = await self.record_repository.create_record(
            CaptchaRecordModel(category_id=category.id, result=parse_result, success=success),
            captcha_files
        )
        return record
