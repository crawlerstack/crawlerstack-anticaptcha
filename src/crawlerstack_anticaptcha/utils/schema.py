"""Schema"""
from enum import Enum

from pydantic import BaseModel  # pylint:disable=no-name-in-module


class MessageData(BaseModel):
    """MessageData"""
    file_id: str
    value: int | str
    category: str


class Message(BaseModel):
    """Message"""
    code: int
    data: MessageData | list = None
    message: str


class Captcha(Enum):
    """SliderCategory"""
    Slider = 'SliderCaptcha'
    Numerical = 'NumericalCaptcha'
    Rotated = 'RotatedCaptcha'
