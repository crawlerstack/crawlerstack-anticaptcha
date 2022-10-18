"""Captcha Factory"""
import logging
from pathlib import Path

from crawlerstack_anticaptcha.captcha.numerical.captcha import NumCaptcha
from crawlerstack_anticaptcha.captcha.slider.captcha import SliderCaptcha
from crawlerstack_anticaptcha.repositories.respositorie import \
    CaptchaRepository
from crawlerstack_anticaptcha.utils.exception import SliderCaptchaParseFailed


class SliderCaptchaService:
    """SliderCaptchaService"""
    captcha_repository = CaptchaRepository()

    def __init__(self, file: Path, captcha_id: int, file_uuid: str):
        self.file = file
        self.captcha_id = captcha_id
        self.file_uuid = file_uuid
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def parse(self):
        """parse"""
        image_captcha = SliderCaptcha(self.file)
        res = image_captcha.parse()
        if res == 0:
            await self.captcha_repository.create(
                file_id=self.file_uuid, category_id=self.captcha_id,
                file_type=str(self.file).split('.')[1],
                success=False
            )
            raise SliderCaptchaParseFailed()
        return res


class NumericalCaptchaService:
    """NumericalCaptchaService"""
    captcha_repository = CaptchaRepository()

    def __init__(self, file: Path, captcha_id: int, file_uuid: str):
        self.file = file
        self.captcha_id = captcha_id
        self.file_uuid = file_uuid
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def parse(self):
        """parse"""
        image_captcha = NumCaptcha(self.file)
        res = image_captcha.parse()
        if res == 0:
            await self.captcha_repository.create(
                file_id=self.file_uuid, category_id=self.captcha_id,
                file_type=str(self.file).split('.')[1],
                success=False
            )
            raise SliderCaptchaParseFailed()
        return res


class RotatedCaptchaService:
    """RotatedCaptchaService"""


class CaptchaFactory:
    """CaptchaFactory"""

    @staticmethod
    def captcha(category: str, file: Path, captcha_id: int, file_uuid: str):
        """
        captcha
        :param file_uuid:
        :param captcha_id:
        :param file:
        :param category:
        :return:
        """
        if category == 'SliderCaptcha':
            return SliderCaptchaService(file, captcha_id, file_uuid)
        if category == 'NumericalCaptcha':
            return NumericalCaptchaService(file, captcha_id, file_uuid)
        return RotatedCaptchaService()
