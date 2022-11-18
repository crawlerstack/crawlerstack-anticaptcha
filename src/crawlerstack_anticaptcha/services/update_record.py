"""Update record"""
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.utils.message import Message


class UpdateRecordService:
    """UpdateRecordService"""

    def __init__(self, success: bool, record_id: str):
        self.success = success
        self.record_id = record_id
        self.captcha_repository = CaptchaRecordRepository()

    async def update(self):
        """update"""
        await self.captcha_repository.update_by_id(self.record_id, success=self.success)
        result = Message(
            code=200, data=None,
            message=f'Update file id is the "success"={self.success} of "{self.record_id}".'
        )
        return result
