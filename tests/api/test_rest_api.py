"""Test api"""
import uvicorn

from crawlerstack_anticaptcha.api.rest_api import start
from crawlerstack_anticaptcha.repositories.record import \
    CaptchaRecordRepository
from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.utils.schema import Message


def test_anticaptcha(mocker, client, mock_path):
    """test anticaptcha"""
    mocker.patch.object(CaptchaService, 'check', return_value=Message(code=20, data=None, message='test'))
    with open(mock_path / 'foo.png', 'wb') as f:
        f.write(bytes(1))
    with open(mock_path / 'foo.png', 'rb') as f:
        files = {'image': f.read()}
        response = client.post(
            '/v1/api/captcha/identify/',
            files=files,
            data={'category': 'SliderCaptcha'}
        )
        assert response.status_code == 200
        assert response.json() == {'code': 20, 'data': None, 'message': 'test'}


def test_record(mocker, client):
    """test record"""
    payload = {"success": False}
    update = mocker.patch.object(CaptchaRecordRepository, 'update_by_pk')
    response = client.put(
        '/v1/api/captcha/record/123',
        data=payload
    )
    assert response.status_code == 200
    update.assert_called_with('123', False)
    assert response.json() == {
        'code': 200, 'data': None,
        'message': 'Update file id is the "success"=False of "123".'}


def test_start(mocker):
    """test start"""
    run = mocker.patch.object(uvicorn, 'run')
    start('foo', 8080)
    run.assert_called()
