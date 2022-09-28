"""response handler"""
import datetime
import logging
import uuid
from pathlib import PurePath

from fastapi import File

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.models import CategoryModel
from crawlerstack_anticaptcha.repositories.respositories import (
    CaptchaRepository, CategoryRepository)
from crawlerstack_anticaptcha.utils.exception import (ObjectDoesNotExist,
                                                      ParsingFailed,
                                                      UnsupportedMediaType)
from crawlerstack_anticaptcha.utils.schema import Message, MessageData
from crawlerstack_anticaptcha.utils.upload_file import UploadedFile

captcha_repository = CaptchaRepository()
category_repository = CategoryRepository()


class CaptchaService:
    """SliderCaptchaHandlerService"""

    def __init__(
            self, file: File, category: str, file_data: bytes
    ):
        self.file = file
        self.category = category
        self.file_data = file_data
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def check(self) -> Message:
        """check"""
        captcha = await self.check_category()
        file_type = self.file.content_type
        file_uuid = str(uuid.uuid1())
        if 'image' in file_type:
            upload_file = UploadedFile(
                self.file_data, captcha,
                f'{file_uuid}.{PurePath(file_type).stem}'
            )
            img_file = upload_file.save()
            image_captcha = SliderCaptcha(str(img_file))
            parse_res = image_captcha.parse()
            if parse_res == 0:
                await self.write_to_db(
                    file_id=file_uuid, category_id=captcha.id,
                    file_type=PurePath(file_type).stem,
                    creation_time=datetime.datetime.today(), success=False
                )
                raise ParsingFailed()
            result_message = Message(
                code=200,
                data=MessageData(
                    value=parse_res,
                    category=captcha.name,
                    file_id=file_uuid
                ),
                message='File parsing succeeded'
            )
            await self.write_to_db(file_id=file_uuid, category_id=captcha.id,
                                   file_type=file_type.split('/')[1],
                                   creation_time=datetime.datetime.today(), success=None)
            return result_message

        if 'image' not in file_type:
            raise UnsupportedMediaType(
                content='The upload file format is incorrect,please upload the correct image type',
                media_type=file_type
            )
        raise ObjectDoesNotExist('No captcha type found, Please upload correctly')

    @staticmethod
    async def write_to_db(**kwargs):
        """
        write_to_db
        :param kwargs:
        """
        await captcha_repository.create(**kwargs)

    async def check_category(self) -> CategoryModel | ObjectDoesNotExist:
        """
        check category
        :return:
        """
        _category: CategoryModel = await category_repository.get_by_name(self.category)
        if _category is None:
            raise ObjectDoesNotExist('No captcha type found, Please upload correctly')
        return _category
