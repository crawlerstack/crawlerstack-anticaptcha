"""api service"""
import logging

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from crawlerstack_anticaptcha.repositories.respositories import \
    CaptchaRepository
from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.utils.schema import RecordItem

logger = logging.getLogger(f'{__name__}  {__name__}')
app = FastAPI()


@app.post(
    '/crawlerstack/captcha/identify/',
    summary='Captcha identify the interface'
)
async def anticaptcha(
        category: str = Form(),
        file: UploadFile = File()
):
    """
    anticaptcha
    :param file:
    :param category:
    :return:
    """
    data = await file.read()
    captcha_service = CaptchaService(file, category, data)
    result_message = await captcha_service.check()
    if result_message.code != 200:
        raise HTTPException(status_code=415, detail=result_message)
    return result_message


@app.put(
    '/crawlerstack/captcha/record/{file_id}',
    summary='The interface that counts whether the captcha is parsed successfully'
)
async def record(file_id: str, item: RecordItem):
    """
    receive
    :param file_id:
    :param item:
    :return:
    """
    captcha_repository = CaptchaRepository()
    await captcha_repository.update(file_id, item.success)
    return {'file_id': file_id, 'item': item}


def start(host: str, port: int):
    """
    start
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
