"""LocalStorages"""
import asyncio
import os

from crawlerstack_anticaptcha.storages.base import BaseStorage


class LocalStorages(BaseStorage):
    """LocalStorages"""

    async def save(self, name: str, file_type: str, data: bytes):
        """save"""
        file_path = self.file(name, file_type)
        try:
            await asyncio.to_thread(self.write_to_file, file_path, data)
        except FileNotFoundError:
            os.makedirs(file_path.parent)
            await asyncio.to_thread(self.write_to_file, file_path, data)
        return file_path

    def write_to_file(self, file, data):
        """write to file"""
        with open(file, 'wb') as obj:
            obj.write(data)
        self.logger.debug('Save file to %s.', file)
