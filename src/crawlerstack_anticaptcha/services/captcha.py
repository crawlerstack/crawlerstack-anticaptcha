"""response handler"""
import logging
import uuid

from pydantic import BaseModel

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


class Message(BaseModel):  # pylint:disable=R0903
    """Message"""
    file_id: uuid.UUID
    success: str
    code: int
    data: dict
    message_text: str


class CaptchaService:  # pylint:disable=R0903
    """SliderCaptchaHandlerService"""

    def __init__(self, file, item_name: int, file_data):
        self.file = file
        self.item_name = item_name
        self.file_data = file_data
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def check(self) -> Message:
        """check"""
        file_type = self.file.content_type
        filename_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, self.file.filename.split('.')[0])
        if 'image' not in file_type:
            result_message = Message(
                file_id=filename_uuid,
                success='false',
                code=415,
                data={
                    'parse_results': '',
                    'media_type': file_type,
                    'captcha_type': '',
                    'captcha_code': ''
                },
                message_text='The upload file format is incorrect,'
                             'please upload the correct image type'
            )

            return result_message

        if 'image' in file_type and self.item_name == 1:
            upload_file = UploadedFile(self.file_data, 'Slider-Captcha',
                                       f'{filename_uuid}.{self.file.filename.split(".")[1]}')
            img_file = upload_file.save()
            image_captcha = SliderCaptcha(str(img_file))
            parse_res = image_captcha.parse()
            result_message = Message(
                file_id=filename_uuid,
                success='true',
                code=200,
                data={
                    'parse_results': parse_res,
                    'media_type': file_type,
                    'captcha_type': 'SliderCaptcha',
                    'captcha_code': 1
                },
                message_text='File parsing succeeded'
            )
            return result_message

        return Message(
            file_id=filename_uuid,
            success='false',
            code=0,
            data={},
            message_text=''
        )
