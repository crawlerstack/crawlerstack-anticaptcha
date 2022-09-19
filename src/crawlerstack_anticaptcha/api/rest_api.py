"""api service"""
import json
import logging

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from crawlerstack_anticaptcha.services.captcha import CaptchaService

logger = logging.getLogger(f'{__name__}  {__name__}')
app = FastAPI()


class RecordingItem(BaseModel):  # pylint:disable=R0903
    """RecordingItem"""
    item_name: int = Form()
    success: str = Form()


@app.post(
    '/crawlerstack/captcha/identify/',
    summary='Captcha identify the interface'
)
async def anticaptcha(
        item_name: int = Form(),
        file: UploadFile = File()
):
    """
    anticaptcha
    :param file:
    :param item_name:
    :return:
    """
    data = await file.read()
    res_handler = CaptchaService(file, int(item_name), data)
    result_message = res_handler.check()
    if result_message.success == 'false':
        raise HTTPException(status_code=415, detail=json.loads(result_message.json()))
    return result_message


@app.put(
    '/crawlerstack/captcha/record/{file_id}',
    summary='The interface that counts whether the captcha is parsed successfully'
)
async def record(file_id: str, item: RecordingItem):
    """
    receive
    :param file_id:
    :param item:
    :return:
    """
    return {'file_id': file_id, 'item': item}


def start(host: str, port: int):
    """
    start
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
