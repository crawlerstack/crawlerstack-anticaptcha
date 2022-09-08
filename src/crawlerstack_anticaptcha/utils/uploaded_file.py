"""Uploaded file"""
import logging
import os
from pathlib import Path

from crawlerstack_anticaptcha.config import settings


class UploadedFile:
    """UploadFile"""
    DOWNLOAD_PATH = settings.IMAGE_DOWNLOAD_PATH

    def __init__(self, data, file_name: str):
        self.data = data
        self.file_name = file_name
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def save(self):
        """download"""
        try:
            self.write_to_file()
        except FileNotFoundError:
            self.logger.info('"FileNotFoundError" Mkdir %s', self.DOWNLOAD_PATH)
            os.makedirs(Path(f'{self.DOWNLOAD_PATH}'))
            self.write_to_file()

    def write_to_file(self):
        """write to file"""
        file = Path(f'{self.DOWNLOAD_PATH}/{self.file_name}')
        with open(file, 'wb') as obj:
            obj.write(self.data)
        self.logger.info('File %s Download Complete.', file)
