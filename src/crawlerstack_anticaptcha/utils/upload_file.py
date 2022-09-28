"""Uploaded file"""
import asyncio
import logging
import os
from pathlib import Path


class UploadedFile:
    """UploadFile"""

    def __init__(self, data: bytes, file: Path):
        self.data = data
        self.file = file
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def save(self):
        """save"""
        try:
            await asyncio.to_thread(self.write_to_file)
        except FileNotFoundError:
            os.makedirs(self.file.parent)
            await asyncio.to_thread(self.write_to_file)

    def write_to_file(self):
        """write to file"""
        with open(self.file, 'wb') as obj:
            obj.write(self.data)
        self.logger.info('File %s Save Complete.', self.file)
