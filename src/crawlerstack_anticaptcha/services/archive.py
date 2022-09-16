"""archive service"""
import logging
import os
import time
from pathlib import Path

from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.repositories.mongo_repository import \
    MongoRepository
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


class ArchiveService:
    """ArchiveService"""

    def __init__(self, file, file_data, success: str, item_name: int):
        self.file = file
        self.file_data = file_data
        self.success = success
        self.item_name = item_name
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def received_info(self):
        """received information"""
        captcha_type = ''
        if self.item_name == 1:
            captcha_type = 'SliderCaptcha'
        return {
            'success': self.success,
            'file': str(self.save_file()),
            'created_at': time.strftime("%Y%m%d%H%M%S", time.localtime()),
            "type": self.file.content_type,
            'captcha_type': captcha_type
        }

    def written_to_db(self):
        """archive file info"""
        mongo = MongoRepository('ParseResults')
        info = self.received_info()
        mongo.write(info)

    def save_file(self):
        """ save file"""
        self.logger.info('Archive file')
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file = f'{timestamp}.{self.file.filename.split(".")[1]}'
        if self.check(self.file_data):
            upload_file = UploadedFile(self.file_data, 'Archive', file)
            image_file = upload_file.save()
            return image_file
        return ''

    def check(self, data):
        """
        check
        :param data:
        :return:
        """
        for file in os.listdir(Path(f'{settings.IMAGE_SAVE_PATH}/Archive')):
            if not os.path.isdir(file):
                with open(file, 'rb') as obj:
                    if obj.read() == data:
                        self.logger.info('File already exists.')
                        return False
                    return True
            return False
