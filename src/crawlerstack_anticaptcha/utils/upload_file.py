"""Uploaded file"""
import logging
import os
from pathlib import Path

from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.models import CategoryModel


class UploadedFile:
    """UploadFile"""
    IMAGE_SAVE_PATH = settings.IMAGE_SAVE_PATH

    def __init__(self, data: bytes, category: CategoryModel, file_name: str):
        self.data = data
        self.file_name = file_name
        self.category = category
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def save(self):
        """save file"""
        try:
            return self.write_to_file()
        except FileNotFoundError:
            self.logger.info('"FileNotFoundError" Mkdir %s', self.IMAGE_SAVE_PATH)
            os.makedirs(Path(self.category.path))
            return self.write_to_file()

    def write_to_file(self):
        """write to file"""
        file = Path(
            self.category.path).joinpath(Path(self.file_name))
        with open(file, 'wb') as obj:
            obj.write(self.data)
        self.logger.info('File %s Save Complete.', file)
        return file
