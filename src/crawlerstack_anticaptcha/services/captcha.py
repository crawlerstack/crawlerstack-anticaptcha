"""response handler"""
import datetime
import logging
import uuid

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.repositories.respositories import (
    CaptchaRepository, CategoryRepository)
from crawlerstack_anticaptcha.utils.schema import Message, MessageData
from crawlerstack_anticaptcha.utils.upload_file import UploadedFile

captcha_repository = CaptchaRepository()
category_repository = CategoryRepository()


class CaptchaService:
    """SliderCaptchaHandlerService"""

    def __init__(
            self, file, category, file_data
    ):
        self.file = file
        self.category = category
        self.file_data = file_data
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def check(self) -> Message:
        """check"""
        try:
            category_id = self.category.ID.value
            category_type = await category_repository.get_by_id(int(category_id))
            file_type = self.file.content_type
            file_uuid = str(uuid.uuid1())
            if 'image' in file_type:
                if self.category.CATEGORY.value == category_type.type:
                    upload_file = UploadedFile(
                        self.file_data,
                        self.category,
                        f'{file_uuid}.{self.file.filename.split(".")[1]}'
                    )
                    img_file = upload_file.save()
                    image_captcha = SliderCaptcha(str(img_file))
                    parse_res = image_captcha.parse()
                    result_message = Message(
                        code=200,
                        data=MessageData(
                            value=parse_res,
                            category=self.category.CATEGORY.value,
                            file_id=file_uuid
                        ),
                        message='File parsing succeeded'
                    )
                    await self.write_to_db(
                        file_id=file_uuid, category_id=1, file_path=str(img_file),
                        file_type=file_type, creation_time=datetime.datetime.today(), success=None
                    )
                    return result_message
                raise ModuleNotFoundError
            if 'image' not in file_type:
                result_message = Message(
                    code=415,
                    data=None,
                    message='The upload file format is incorrect,'
                            'please upload the correct image type'
                )
                return result_message
            return Message(code=0, data=None, message='')
        except ModuleNotFoundError:
            return Message(code=0, data=None, message='ModuleNotFoundError')

    async def write_to_db(self, /, **kwargs):
        """
        write_to_db
        :param kwargs:
        """
        await captcha_repository.create(**kwargs)
