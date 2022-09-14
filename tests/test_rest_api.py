"""Test api"""
import pytest
from fastapi.testclient import TestClient

from crawlerstack_anticaptcha.api.rest_api import app
from crawlerstack_anticaptcha.services.handler import HandlerService

client = TestClient(app)


@pytest.mark.parametrize(
    'success',
    [
        'false',
        'true'
    ]
)
def test_post(mocker, success):
    """
    test_post
    :param mocker:
    :param success:
    :return:
    """
    if success == 'true':
        check = mocker.patch.object(HandlerService, 'check')
        payload = {'item_name': '1'}
        files = [('file', ('下载 (4).png', open(mocker.MagicMock(), 'rb'), 'image/png'))]  # pylint:disable=R1732
        response = client.post(
            '/crawlerstack/anticaptcha/',
            data=payload,
            files=files
        )
        assert response.status_code == 200
        check.assert_called_with()

    if success == 'false':
        payload = {'item_name': '1'}
        files = [('file', ('test.json', open(mocker.MagicMock(), 'rb'), 'application/json'))]  # pylint:disable=R1732
        res_handler = HandlerService(mocker.MagicMock(), 1, mocker.MagicMock())
        res_handler.check = mocker.MagicMock(rtetutn_value={'success': 'false'})

        response = client.post(
            '/crawlerstack/anticaptcha/',
            data=payload,
            files=files
        )
        assert response.status_code == 415
