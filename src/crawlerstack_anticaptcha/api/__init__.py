"""exception_handler"""
from fastapi import Request
from fastapi.responses import JSONResponse

from crawlerstack_anticaptcha.api.rest_api import app
from crawlerstack_anticaptcha.utils.exception import (CaptchaParseFailed,
                                                      ObjectDoesNotExist,
                                                      UnsupportedMediaType)
from crawlerstack_anticaptcha.utils.message import Message


@app.exception_handler(ObjectDoesNotExist)
async def not_exist_exception_handler(
        _: Request,
        exc: ObjectDoesNotExist
):
    """
    not_exist_exception_handler
    :param _:
    :param exc:
    :return:
    """
    result = Message(
        code=404,
        data=None,
        message=exc.content
    )
    return JSONResponse(
        status_code=404,
        content=result.dict(),
    )


@app.exception_handler(UnsupportedMediaType)
async def unsupported_type_exception_handler(
        _: Request,
        exc: UnsupportedMediaType
):
    """
    unsupported_type_exception_handler
    :param _:
    :param exc:
    :return:
    """
    result = Message(
        code=415,
        data=None,
        message=exc.content
    )
    return JSONResponse(
        status_code=415,
        content=result.dict(),
    )


@app.exception_handler(CaptchaParseFailed)
async def numerical_parse_failed_exception_handler(
        _: Request,
        exc: CaptchaParseFailed
):
    """
    numerical_parse_failed_exception_handler
    :param _:
    :param exc:
    :return:
    """
    result = Message(
        code=422,
        data=None,
        message=exc.content
    )
    return JSONResponse(
        status_code=422,
        content=result.dict(),
    )
