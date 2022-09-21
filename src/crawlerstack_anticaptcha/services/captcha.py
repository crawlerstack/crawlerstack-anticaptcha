"""response handler"""
import datetime
import logging
import uuid

from sqlalchemy.exc import IntegrityError

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.repositories.respositories import (
    CaptchaRepository, CategoryRepository)
from crawlerstack_anticaptcha.utils.schema import Message, MessageData
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


class CaptchaService:  # pylint:disable=R0903
    """SliderCaptchaHandlerService"""

    def __init__(self, file, category_name: str, file_data):
        self.file = file
        self.category_name = category_name
        self.file_data = file_data
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def check(self) -> Message:
        """check"""
        file_type = self.file.content_type
        file_uuid = str(uuid.uuid1())
        if 'image' not in file_type:
            result_message = Message(
                code=415,
                data=None,
                message='The upload file format is incorrect,'
                        'please upload the correct image type'
            )
            return result_message

        if 'image' in file_type and self.category_name == 'SliderCaptcha':
            upload_file = UploadedFile(self.file_data, 'Slider-Captcha',
                                       f'{file_uuid}.{self.file.filename.split(".")[1]}')
            img_file = upload_file.save()
            image_captcha = SliderCaptcha(str(img_file))
            parse_res = image_captcha.parse()
            result_message = Message(
                code=200,
                data=MessageData(value=parse_res, category=self.category_name, file_id=file_uuid),
                message='File parsing succeeded'
            )
            await self.written_to_db(
                file_id=file_uuid,
                category_id=1,
                file_path=str(img_file),
                file_type=file_type,
                creation_time=datetime.datetime.today(),
                success=None
            )
            return result_message

        if 'image' in file_type and self.category_name == 'RotatedCaptcha':
            upload_file = UploadedFile(self.file_data, 'Rotated-Captcha',
                                       f'{file_uuid}.{self.file.filename.split(".")[1]}')
            img_file = upload_file.save()
            image_captcha = SliderCaptcha(str(img_file))
            parse_res = image_captcha.parse()
            result_message = Message(
                code=200,
                data=MessageData(value=parse_res, category=self.category_name, file_id=file_uuid),
                message='File parsing succeeded'
            )
            await self.written_to_db(
                file_id=file_uuid,
                category_id=2,
                file_path=str(img_file),
                file_type=file_type,
                creation_time=datetime.datetime.today(),
                success=None
            )
            return result_message

        return Message(code=0, data=None, message='')

    async def written_to_db(self, /, **kwargs):
        """
        written_to_db
        :return:
        """
        captcha_repository = CaptchaRepository()
        try:
            await captcha_repository.create(**kwargs)
        except IntegrityError:
            await self.init_category()
            await captcha_repository.create(**kwargs)

    @staticmethod
    async def init_category():
        """init category"""
        category_resp = CategoryRepository()
        await category_resp.add_all()
