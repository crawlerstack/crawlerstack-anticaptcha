"""Test api"""
import json

from crawlerstack_anticaptcha.repositories.respositorie import \
    CaptchaRepository


def test_receive_parse_results(mocker, client):
    """test receive parse results"""
    update = mocker.patch.object(CaptchaRepository, 'update_by_file_id')
    payload = json.dumps({
        "category": 'foo',
        "success": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.put(
        '/crawlerstack/captcha/record/123',
        headers=headers,
        data=payload
    )
    assert response.status_code == 200
    update.assert_called_with('123', False)
