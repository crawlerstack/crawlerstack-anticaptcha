"""response handler"""
import logging
import time

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


class CaptchaService:
    """SliderCaptchaHandlerService"""

    def __init__(self, file, item_name: int, file_data):
        self.file = file
        self.item_name = item_name
        self.file_data = file_data
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def check(self) -> dict:
        """check"""
        file_type = self.file.content_type
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if 'image' not in file_type:
            result_message = self.message(
                'false',
                415,
                {'parse_results': '',
                 'media_type': file_type,
                 'captcha_type': '',
                 'captcha_code': ''
                 },
                'The upload file format is incorrect,please upload the correct image type.'
            )
            return result_message

        if 'image' in file_type and self.item_name == 1:
            upload_file = UploadedFile(self.file_data, 'Slider-Captcha',
                                       f'{timestamp}.{self.file.filename.split(".")[1]}')
            img_file = upload_file.save()
            image_captcha = SliderCaptcha(str(img_file))
            parse_res = image_captcha.parse()
            result_message = self.message(
                'true',
                200,
                {'parse_results': parse_res,
                 'media_type': file_type,
                 'captcha_type': 'SliderCaptcha',
                 'captcha_code': 1
                 },
                'File parsing succeeded.'
            )
            return result_message

        return {
            'success': 'false',
            'code': '',
            'data': '',
            'message': ''
        }

    @staticmethod
    def message(success: str, code: int, data: dict, message_text: str):
        """message"""
        return {
            'success': success,
            'code': code,
            'data': data,
            'message': message_text
        }
