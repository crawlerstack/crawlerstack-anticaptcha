"""test storages api"""
from crawlerstack_anticaptcha.repositories.storage import StorageRepository
from crawlerstack_anticaptcha.services.storage import StorageService
from crawlerstack_anticaptcha.utils.schema import Message


def test_update_storage(mocker, client):
    """test_update_storage"""
    update_by_id = mocker.patch.object(StorageRepository, 'update_by_id')
    response = client.patch(
        '/api/v1/captcha/storages/1',
        data={'default': False}
    )
    assert response.status_code == 200
    update_by_id.assert_called_with(1, default=False)
    assert response.json() == {'code': 200, 'data': None, 'message': 'ok'}


def test_delete_storage(mocker, client):
    """test_delete_storage"""
    delete_by_id = mocker.patch.object(StorageRepository, 'delete_by_id')
    response = client.delete('/api/v1/captcha/storages/1')
    assert response.status_code == 200
    delete_by_id.assert_called_with(1)
    assert response.json() == {'code': 200, 'data': None, 'message': 'ok'}


def test_create_storage_config(mocker, client):
    """test_create_storage_config"""
    payload = {'name': 'bar', 'uri': 'foo'}
    mocker.patch.object(
        StorageService,
        'create',
        return_value=Message(code=200, data=None, message='create successfully'))
    response = client.post(
        '/api/v1/captcha/storages',
        data=payload
    )
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'data': None, 'message': 'create successfully'}


def test_get_storage_by_id(mocker, client):
    """test_get_storage_by_id"""
    mocker.patch.object(StorageRepository, 'get_by_id', return_value=None)
    response = client.get('/api/v1/captcha/storages/1')
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'data': None, 'message': 'Details with id 1'}


def test_get_all_storages(mocker, client):
    """test_get_all_storages"""
    mocker.patch.object(
        StorageService,
        'get_all',
        return_value=Message(code=200, data=None, message='Available storage methods.')
    )
    response = client.get('/api/v1/captcha/storages')
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'data': None, 'message': 'Available storage methods.'}
