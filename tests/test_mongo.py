"""Test mongo"""
from crawlerstack_anticaptcha.repositories.mongo_repository import \
    MongoRepository


def test_write():
    """test_write"""
    mongo = MongoRepository('foo')
    mongo.db_name = 'test'
    if 'foo' in mongo.mongo_client['test'].list_collection_names():
        mongo.delete()

    mongo.write({'foo': 'bar'})
    result = mongo.read()
    assert list(result)[0].get('foo') == 'bar'
