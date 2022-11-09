"""CaptchaFileRepository"""

from crawlerstack_anticaptcha.models import CaptchaFileModel
from crawlerstack_anticaptcha.repositories.base import BaseRepository


class CaptchaFileRepository(BaseRepository):
    """CaptchaFileRepository"""

    @property
    def model(self):
        """model"""
        return CaptchaFileModel
