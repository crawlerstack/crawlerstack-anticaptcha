"""exception_handler"""
from fastapi import Request
from fastapi.responses import JSONResponse

from crawlerstack_anticaptcha.api.rest_api import app
from crawlerstack_anticaptcha.utils.exception import (ObjectDoesNotExist,
                                                      ObjectIndexError,
                                                      ParsingFailed,
                                                      UnsupportedMediaType)


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
    return JSONResponse(
        status_code=404,
        content={"message": exc.content},
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
    return JSONResponse(
        status_code=415,
        content={"message": exc.content, 'type': exc.media_type},
    )


@app.exception_handler(ParsingFailed)
async def parsing_failed_exception_handler(
        _: Request,
        exc: ParsingFailed
):
    """
    parsing failed exception handler
    :param _:
    :param exc:
    :return:
    """
    return JSONResponse(content={"message": exc.content})


@app.exception_handler(ParsingFailed)
async def index_error_exception_handler(
        _: Request,
        exc: ObjectIndexError
):
    """
    parsing failed exception handler
    :param _:
    :param exc:
    :return:
    """
    return JSONResponse(status_code=404, content={"message": exc.content})
