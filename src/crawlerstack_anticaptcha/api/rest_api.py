"""api service"""
import logging

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.services.update_record import UpdateRecordService
from crawlerstack_anticaptcha.utils.exception import ObjectDoesNotExist
from crawlerstack_anticaptcha.utils.schema import RecordItem

logger = logging.getLogger(f'{__name__}  {__name__}')
app = FastAPI()


@app.exception_handler(ObjectDoesNotExist)
async def exception_handler(request: Request, exc: ObjectDoesNotExist):  # pylint:disable=unused-argument
    """
    exception_handler
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=404,
        content={"message": exc.content},
    )


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
    if result_message.code != 200:
        raise HTTPException(status_code=415, detail=result_message)
    return result_message


@app.put('/crawlerstack/captcha/record/{file_id}')
async def record(file_id: str, item: RecordItem):
    """
    The interface that counts whether the captcha is parsed successfully
    """
    update = UpdateRecordService(item.success, file_id)
    await update.update()
    return {'file_id': file_id, 'item': item}


def start(host: str, port: int):
    """
    start
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
