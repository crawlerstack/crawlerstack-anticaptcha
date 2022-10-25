"""Test api"""
import uvicorn

from crawlerstack_anticaptcha.api.rest_api import start
from crawlerstack_anticaptcha.repositories.respositorie import \
    CaptchaRepository
from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.utils.schema import Message


def test_get_category(client, init_category):
    """test get category"""
    response = client.get('/crawlerstack/category/')
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": [
            {'id': 1, 'name': 'SliderCaptcha'},
            {'id': 2, 'name': 'RotatedCaptcha'},
            {'id': 3, 'name': 'NumericalCaptcha'}
        ],
        "message": "The identified captcha category can be provided."
    }


def test_receive_parse_results(mocker, client):
    """test receive parse results"""
    payload = {"success": False}
    update = mocker.patch.object(CaptchaRepository, 'update_by_file_id')
    response = client.put(
        '/crawlerstack/captcha/record/123',
        data=payload
    )
    assert response.status_code == 200
    update.assert_called_with('123', False)


def test_anticaptcha(mocker, client, mock_path):
    """test anticaptcha"""
    mocker.patch.object(CaptchaService, 'check', return_value=Message(code=20, data=None, message='test'))
    with open(mock_path / 'foo.png', 'wb') as f:
        f.write(bytes(1))
    with open(mock_path / 'foo.png', 'rb') as f:
        files = {'file': f.read()}
        response = client.post(
            '/crawlerstack/captcha/identify/',
            files=files,
            data={'category': 'SliderCaptcha'}
        )
        assert response.status_code == 200
        assert response.json() == {'code': 20, 'data': None, 'message': 'test'}


def test_start(mocker):
    """test start"""
    run = mocker.patch.object(uvicorn, 'run')
    start('foo', 8080)
    run.assert_called()
