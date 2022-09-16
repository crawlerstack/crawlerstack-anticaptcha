"""Test handler"""
import pytest

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


def test_message():
    """test message"""
    handler = CaptchaService('test', 1, 'data')
    result = handler.message('foo', 1, {'data': 'bar'}, 'test')
    assert result == {'code': 1, 'data': {'data': 'bar'}, 'message': 'test', 'success': 'foo'}


@pytest.mark.parametrize(
    'test_file,item_name',
    [
        ('image', 1),
        ('image', 0),
        ('foo', 1),
        ('foo', 0)
    ]
)
def test_check(mocker, test_file, item_name):
    """test check"""
    if test_file != 'image':
        test_file = mocker.MagicMock(content_type=test_file)
        file_data = mocker.MagicMock()
        handler = CaptchaService(test_file, item_name, file_data)
        result = handler.check()
        assert result.get('success') == 'false'

    if test_file == 'image' and item_name == 1:
        save = mocker.patch.object(UploadedFile, 'save')
        parse = mocker.patch.object(SliderCaptcha, 'parse')
        test_file = mocker.MagicMock(content_type=test_file)
        file_data = mocker.MagicMock()
        handler = CaptchaService(test_file, item_name, file_data)
        result = handler.check()
        save.assert_called()
        parse.assert_called()
        assert result.get('success') == 'true'

    if test_file == 'image' and item_name == 0:
        test_file = mocker.MagicMock(content_type=test_file)
        file_data = mocker.MagicMock()
        handler = CaptchaService(test_file, item_name, file_data)
        result = handler.check()
        assert result.get('success') == 'false'

    else:
        test_file = mocker.MagicMock(content_type=test_file)
        file_data = mocker.MagicMock()
        handler = CaptchaService(test_file, item_name, file_data)
        result = handler.check()
        assert result.get('success') == 'false'
