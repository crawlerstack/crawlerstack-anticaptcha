"""Schema"""
from enum import Enum

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class MessageData(BaseModel):
    """MessageData"""
    id: str
    value: int | str
    category: str


class Message(BaseModel):
    """Message"""
    code: int
    data: MessageData | list | object = None
    message: str


class Captcha(Enum):
    """CaptchaCategory"""
    Slider = 'SliderCaptcha'
    Numerical = 'NumericalCaptcha'
    Rotated = 'RotatedCaptcha'


class CaptchaPath(Enum):
    """CaptchaPath"""
    Slider = 'slider-captcha'
    Numerical = 'numerical-captcha'
    Rotated = 'rotated-captcha'
