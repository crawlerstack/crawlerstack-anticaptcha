"""api service"""
import logging

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile

from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.services.category import CategoryService
from crawlerstack_anticaptcha.services.update_record import UpdateRecordService

logger = logging.getLogger(f'{__name__}  {__name__}')
app = FastAPI()


@app.get('/crawlerstack/category/')
async def get_category():
    """Query captcha category list"""
    category = CategoryService()
    return await category.get_all()


@app.post('/crawlerstack/captcha/identify/')
async def anticaptcha(
        category: str = Form(),
        file: UploadFile = File()
):
    """
    Captcha identify the interface
    """
    data = await file.read()
    captcha_service = CaptchaService(file, category, data)
    result_message = await captcha_service.check()
    return result_message


@app.put('/crawlerstack/captcha/record/{file_id}')
async def record(file_id: str, success: bool = Form()):
    """
    The interface that counts whether the captcha is parsed successfully
    """
    update = UpdateRecordService(success, file_id)
    result = await update.update()
    return result


def start(host: str, port: int):
    """
    start
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
