"""Test api"""

from crawlerstack_anticaptcha.repositories.respositorie import \
    CaptchaRepository


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
