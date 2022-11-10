"""storage"""

from threading import Lock

from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.models import StorageModel
from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.storages.local import LocalStorages


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class StorageFactory(metaclass=SingletonMeta):
    """StorageFactory"""

    def __init__(self, storage_name: str = 'local'):
        self.name = storage_name
        self.storage = None

    async def default(self) -> StorageModel:
        """获取存储配置"""
        if not self.storage:
            storage = StorageRepository()
            default = await storage.get_default()
            if default:
                self.storage = default
            else:
                self.storage = StorageModel(uri=settings.CAPTCHA_IMAGE_PATH, id=0)

    async def factory(self, data, file_name: str, file_type: str):
        """storage_factory"""
        storage_instance = None
        await self.default()
        if self.name == 'local':
            storage_instance = LocalStorages(self.storage)
        file = await storage_instance.save(file_name, file_type, data)
        return {'file': file, 'id': self.storage.id}
