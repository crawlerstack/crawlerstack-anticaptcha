"""api service"""
import logging

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from crawlerstack_anticaptcha.services.handler import HandlerService

logger = logging.getLogger(f'{__name__}  {__name__}')
app = FastAPI()


@app.post('/crawlerstack/anticaptcha/')
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
    res_handler = HandlerService(file, item_name, data)
    result_message = res_handler.check()
    if result_message.get('success') == 'false':
        raise HTTPException(status_code=415, detail=result_message)

    return result_message


def run(host: str, port: int):
    """
    run
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
