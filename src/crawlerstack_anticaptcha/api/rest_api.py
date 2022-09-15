"""api service"""
import logging

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from crawlerstack_anticaptcha.services.archive import ArchiveService
from crawlerstack_anticaptcha.services.captcha import CaptchaService

logger = logging.getLogger(f'{__name__}  {__name__}')
app = FastAPI()


@app.post('/crawlerstack/identify_captcha/')
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
    if result_message.get('success') == 'false':
        raise HTTPException(status_code=415, detail=result_message)
    return result_message


@app.post('/crawlerstack/record_results/')
async def receive_parse_results(
        item_name: int = Form(),
        file: UploadFile = File(),
        success: str = Form()
):
    """
    receive
    :param item_name:
    :param file:
    :param success:
    :return:
    """
    data = await file.read()
    archive = ArchiveService(file, data, success, item_name)
    archive.written_to_db()
    return archive.received_info()


def start(host: str, port: int):
    """
    start
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
