"""storage service"""
from datetime import datetime

from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.utils.schema import Message


class StorageService:
    """StorageService"""
    storage_repository = StorageRepository()

    def __init__(self, storage_id: int = None, name: str = None, uri: str = None, default: bool = False):
        self.storage_id = storage_id
        self.name = name
        self.uri = uri
        self.default = default
        self.now = datetime.now()

    async def create(self):
        """create storage"""
        obj = await self.storage_repository.create(
            uri=self.uri,
            name=self.name,
            default=self.default,
        )
        return Message(
            code=200,
            data=obj,
            message=f'<{self.name}> create successfully'
        )

    async def update(self):
        """update storage config"""
        await self.storage_repository.update_by_id(self.storage_id, default=self.default)
        return Message(
            code=200,
            message='ok'
        )

    async def get_all(self):
        """get all"""
        storages_list = []
        for i in await self.storage_repository.get_all():
            storages_list.append(
                {'id': i.id, 'name': i.name, 'uri': i.uri}
            )
        return Message(
            code=200,
            data=storages_list,
            message='Available storage methods.'
        )

    async def get_by_id(self):
        """get by id"""
        result = await self.storage_repository.get_by_id(self.storage_id)
        return Message(
            code=200,
            data=result,
            message=f'Details with id {self.storage_id}'
        )

    async def delete_by_id(self):
        """delete by id"""
        await self.storage_repository.delete_by_id(self.storage_id)
        return Message(
            code=200,
            message='ok'
        )
