"""api service"""
import uvicorn
from fastapi import FastAPI

from .captcha_api import router

app = FastAPI()
app.include_router(router, prefix='/api/v1/captcha')


def start(host: str, port: int):
    """
    start
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)
