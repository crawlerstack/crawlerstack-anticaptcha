"""test category api"""
from crawlerstack_anticaptcha.repositories.category import CategoryRepository


def test_create_captcha_category(mocker, client):
    """test_create_captcha_category"""
    payload = {'name': 'foo'}
    create = mocker.patch.object(CategoryRepository, 'create')
    response = client.post(
        '/api/v1/captcha/categories',
        data=payload
    )
    assert response.status_code == 200
    create.assert_called()
    assert response.json() == {"code": 200, "data": None, "message": "ok"}


def test_update_captcha_category(mocker, client):
    """test_update_captcha_category"""
    update_by_id = mocker.patch.object(CategoryRepository, 'update_by_id')
    response = client.patch(
        '/api/v1/captcha/categories/1',
        data={'name': 'bar'}
    )
    assert response.status_code == 200
    update_by_id.assert_called_with(1, name='bar')
    assert response.json() == {'code': 200, 'data': None, 'message': 'ok'}


def test_get_category(client):
    """test get category"""
    response = client.get('/api/v1/captcha/categories')
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'data': [],
        'message': 'The identified captcha category can be provided.'}
