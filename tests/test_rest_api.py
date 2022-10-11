"""Test api"""

from crawlerstack_anticaptcha.repositories.respositorie import \
    CaptchaRepository


def test_get_category(client, init_category):
    """test get category"""
    response = client.get('/crawlerstack/category/query/')
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": [
            {"id": 1, "name": "SliderCaptcha"},
            {"id": 2, "name": "RotatedCaptcha"}
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
