"""Update record"""
from crawlerstack_anticaptcha.repositories.respositorie import \
    CaptchaRepository


class UpdateRecordService:
    """UpdateRecordService"""

    def __init__(self, success: bool, file_id: str):
        self.success = success
        self.file_id = file_id
        self.captcha_repository = CaptchaRepository()

    async def update(self):
        """update"""
        await self.captcha_repository.update_by_file_id(
            self.file_id,
            self.success
        )
