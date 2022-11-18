"""Base"""
import logging

from crawlerstack_anticaptcha.models import StorageModel


class BaseStorage:
    """Base Storage"""
    instance = None

    def __init__(self, storage: StorageModel):
        self.storage = storage
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def save(self, name: str, file_type: str, data: bytes):
        """save"""
        raise NotImplementedError
