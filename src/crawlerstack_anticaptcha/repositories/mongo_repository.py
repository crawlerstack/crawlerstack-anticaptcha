"""Mongo Repository"""
import logging

from pymongo import MongoClient
from pymongo.collection import Collection

from crawlerstack_anticaptcha.config import settings


class MongoRepository:
    """Mongo Repository"""

    def __init__(self, collection_name: str):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.collection_name = collection_name
        self.mongo_client = MongoClient(settings.MONGODB_URL)
        self.db_name = settings.MONGODB_NAME

    @property
    def collection(self) -> Collection:
        """
        collection
        :return:
        """
        collection = self.mongo_client.get_database(
            self.db_name).get_collection(self.collection_name)
        return collection

    def write(self, content: dict):
        """
        write
        :param content:
        :return:
        """

        self.collection.insert_one(content)
        self.logger.info('%s written to %s', content, self.collection_name)

    def read(self):
        """
        read
        :return:
        """
        data = self.collection.find()

        return data

    def delete(self):
        """
        delete
        :return:
        """
        self.collection.drop()
