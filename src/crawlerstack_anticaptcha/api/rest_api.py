"""api service"""
import logging

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from crawlerstack_anticaptcha.repositories.respositories import \
    CaptchaRepository
from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.utils.factory import CaptchaFactory
from crawlerstack_anticaptcha.utils.schema import RecordItem

logger = logging.getLogger(f'{__name__}  {__name__}')
app = FastAPI()


@app.post('/crawlerstack/captcha/identify/')
async def anticaptcha(
        category: str = Form(),
        file: UploadFile = File()
):
    """
    Captcha identify the interface
    """
    data = await file.read()
    factory = CaptchaFactory(category)
    captcha_service = CaptchaService(file, factory.create_captcha(), data)
    result_message = await captcha_service.check()
    if result_message.code != 200:
        raise HTTPException(status_code=415, detail=result_message)
    return result_message


@app.put('/crawlerstack/captcha/record/{file_id}')
async def record(file_id: str, item: RecordItem):
    """
    The interface that counts whether the captcha is parsed successfully
    """
    captcha_repository = CaptchaRepository()
    await captcha_repository.update_by_file_id(file_id, item.success)
    return {'file_id': file_id, 'item': item}


def start(host: str, port: int):
    """
    start
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
