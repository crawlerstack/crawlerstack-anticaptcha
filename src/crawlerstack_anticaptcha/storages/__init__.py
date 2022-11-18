"""storage"""

from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.storages.local import LocalStorages
from crawlerstack_anticaptcha.utils import SingletonMeta


class Storage(metaclass=SingletonMeta):
    """StorageFactory"""
    storage_funcs = {'local': LocalStorages}

    def __init__(self, storage_name: str = 'local'):
        self.name = storage_name
        self.storage = None
        self.storage_repository = StorageRepository()

    async def get_default_storage(self):
        """获取存储配置"""
        if not self.storage:
            await self.storage_repository.init_default()
            default_storage = await self.storage_repository.get_by_name(self.name)
            if default_storage:
                self.storage = default_storage
            else:
                self.name = 'local'
                self.storage = await self.storage_repository.get_by_name(self.name)
            await self.storage_repository.update_by_name(self.name)

    async def factory(self, data, file_name: str, file_type: str):
        """storage_factory"""
        await self.get_default_storage()
        storage_instance = self.storage_funcs.get(self.name)(self.storage)
        file = await storage_instance.save(file_name, file_type, data)
        return {'file': file, 'file_name': file_name, 'file_type': file_type, 'id': self.storage.id}
