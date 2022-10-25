"""test exception handler"""
import pytest

from crawlerstack_anticaptcha.services.category import CategoryService
from crawlerstack_anticaptcha.utils.exception import (CaptchaParseFailed,
                                                      ObjectDoesNotExist,
                                                      UnsupportedMediaType)


@pytest.mark.parametrize(
    'exception',
    [
        ObjectDoesNotExist,
        UnsupportedMediaType,
        CaptchaParseFailed
    ]
)
def test_exception_handler(mocker, client, exception):
    """test_exception_handler"""
    if exception is ObjectDoesNotExist:
        mocker.patch.object(CategoryService, 'get_all', side_effect=exception('test'))
        response = client.get('/crawlerstack/category/')
        assert response.status_code == 404
        assert response.json() == {'code': 404, 'data': None, 'message': 'test'}
    if exception is UnsupportedMediaType:
        mocker.patch.object(CategoryService, 'get_all', side_effect=exception('test'))
        response = client.get('/crawlerstack/category/')
        assert response.status_code == 415
        assert response.json() == {'code': 415, 'data': None, 'message': 'test'}
    if exception is CaptchaParseFailed:
        mocker.patch.object(CategoryService, 'get_all', side_effect=exception)
        response = client.get('/crawlerstack/category/')
        assert response.status_code == 422
        assert response.json() == {'code': 422, 'data': None, 'message': 'Parsing failed, please upload again.'}
