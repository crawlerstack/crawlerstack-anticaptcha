"""Uploaded file"""
import logging
import os
from pathlib import Path

from crawlerstack_anticaptcha.config import settings


class UploadedFile:
    """UploadFile"""
    download_path = settings.IMAGE_DOWNLOAD_PATH

    def __init__(self, data, folder: str, file_name: str):
        self.data = data
        self.file_name = file_name
        self.folder = folder
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def save(self):
        """download"""
        try:
            return self.write_to_file()
        except FileNotFoundError:
            self.logger.info('"FileNotFoundError" Mkdir %s', self.download_path)
            os.makedirs(Path(f'{self.download_path}/{self.folder}'))
            return self.write_to_file()

    def write_to_file(self):
        """write to file"""
        file = Path(f'{self.download_path}/{self.folder}/{self.file_name}')
        with open(file, 'wb') as obj:
            obj.write(self.data)
        self.logger.info('File %s Download Complete.', file)
        return file
