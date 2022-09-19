"""Test handler"""
import uuid

import pytest

from crawlerstack_anticaptcha.captcha_chacker.slider_captcha import \
    SliderCaptcha
from crawlerstack_anticaptcha.services.captcha import CaptchaService, Message
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile


def test_message():
    """test message"""
    result = Message(
        file_id=uuid.uuid3(uuid.NAMESPACE_OID, '1'),
        success='false',
        code=0,
        data={},
        message_text=''
    )
    assert result.success == 'false'


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
        test_file = mocker.MagicMock(content_type=test_file, filename='foo.jpg')
        file_data = mocker.MagicMock()
        handler = CaptchaService(test_file, item_name, file_data)
        result = handler.check()
        assert result.success == 'false'

    if test_file == 'image' and item_name == 1:
        save = mocker.patch.object(UploadedFile, 'save')
        parse = mocker.patch.object(SliderCaptcha, 'parse')
        test_file = mocker.MagicMock(content_type=test_file, filename='foo.jpg')
        file_data = mocker.MagicMock()
        handler = CaptchaService(test_file, item_name, file_data)
        result = handler.check()
        save.assert_called()
        parse.assert_called()
        assert result.success == 'true'

    if test_file == 'image' and item_name == 0:
        test_file = mocker.MagicMock(content_type=test_file, filename='foo.jpg')
        file_data = mocker.MagicMock()
        handler = CaptchaService(test_file, item_name, file_data)
        result = handler.check()
        assert result.success == 'false'

    else:
        test_file = mocker.MagicMock(content_type=test_file, filename='foo.jpg')
        file_data = mocker.MagicMock()
        handler = CaptchaService(test_file, item_name, file_data)
        result = handler.check()
        assert result.success == 'false'
