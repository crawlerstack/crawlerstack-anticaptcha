"""Upload"""
import logging

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile

from crawlerstack_anticaptcha.services.cracker import \
    ImageTransformationServices
from crawlerstack_anticaptcha.utils.uploaded_file import UploadedFile

logger = logging.getLogger(f'{__name__}  {__name__}')
app = FastAPI()


def message(success: str, code: int, data: dict, message_text: str):
    """
    message
    :param message_text:
    :param success:
    :param code:
    :param data:
    :return:
    """
    return {
        'success': success,
        'code': code,
        'data': data,
        'message': message_text
    }


@app.post('/crawlerstack/anticaptcha/')
async def anticaptcha(item_name: int, file: UploadFile):
    """
    anticaptcha
    :param item_name:
    :param file:
    :return:
    """
    file_type = file.content_type
    if 'image' not in file_type:
        result_message = message(
            'false',
            415,
            {'parse_results': '',
             'media_type': file_type,
             'captcha_type': '',
             'captcha_code': ''
             },
            'The upload file format is incorrect,please upload the correct image type.'
        )
        raise HTTPException(status_code=415, detail=result_message)

    if 'image' in file_type:
        data = await file.read()
        upload_file = UploadedFile(data, file.filename)
        upload_file.save()
        if item_name == 1:
            image_captcha = ImageTransformationServices()
            parse_res = image_captcha.parse()
            result_message = message(
                'true',
                200,
                {'parse_results': parse_res,
                 'media_type': file_type,
                 'captcha_type': 'ImageTransformation',
                 'captcha_code': 1
                 },
                'File parsing succeeded.'
            )
            logger.info('Parse the captcha of code 1')
            return result_message


def run(host: str, port: int):
    """
    run
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
