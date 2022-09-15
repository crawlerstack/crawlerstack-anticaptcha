"""Test api"""
import pytest
from fastapi.testclient import TestClient

from crawlerstack_anticaptcha.api.rest_api import app
from crawlerstack_anticaptcha.services.archive import ArchiveService
from crawlerstack_anticaptcha.services.captcha import CaptchaService

client = TestClient(app)


@pytest.mark.parametrize(
    'success',
    [
        'false',
        'true'
    ]
)
def test_post_anticaptcha(mocker, success):
    """
    test_post
    :param mocker:
    :param success:
    :return:
    """
    if success == 'true':
        check = mocker.patch.object(CaptchaService, 'check')
        payload = {'item_name': '1'}
        files = [('file', ('foo.png', open(mocker.MagicMock(), 'rb'), 'image/png'))]  # pylint:disable=R1732
        response = client.post(
            '/crawlerstack/identify_captcha/',
            data=payload,
            files=files
        )
        assert response.status_code == 200
        check.assert_called_with()

    if success == 'false':
        payload = {'item_name': '1'}
        files = [('file', ('test.json', open(mocker.MagicMock(), 'rb'), 'application/json'))]  # pylint:disable=R1732
        res_handler = CaptchaService(mocker.MagicMock(), 1, mocker.MagicMock())
        res_handler.check = mocker.MagicMock(rtetutn_value={'success': 'false'})

        response = client.post(
            '/crawlerstack/identify_captcha/',
            data=payload,
            files=files
        )
        assert response.status_code == 415


def test_receive_parse_results(mocker):
    """test receive parse results"""
    written_to_db = mocker.patch.object(ArchiveService, 'written_to_db')
    mocker.patch.object(ArchiveService, 'received_info', return_value={'foo': 'bar'})
    payload = {'item_name': '1', 'success': 'false'}
    files = [('file', ('foo.png', open(mocker.MagicMock(), 'rb'), 'image/png'))]  # pylint:disable=R1732
    response = client.post(
        '/crawlerstack/record_results/',
        data=payload,
        files=files
    )
    assert response.status_code == 200
    assert response.json() == {'foo': 'bar'}
    written_to_db.assert_called_with()
