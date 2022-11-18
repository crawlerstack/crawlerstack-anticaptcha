"""Schema"""
from enum import Enum

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class MessageData(BaseModel):
    """MessageData"""
    id: int
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


class StorageSchema(BaseModel):
    """StorageSchema"""
    id: int
    uri: str
    name: str
    default: bool

    class Config:
        """Config"""
        orm_mode = True


class CaptchaCategorySchema(BaseModel):
    """CaptchaCategorySchema"""
    id: int
    name: str

    class Config:
        """config"""
        orm_mode = True


class CaptchaRecordSchema(BaseModel):
    """CaptchaRecordSchema"""
    id: int
    category_id: int
    content: str | None
    result: str
    success: bool | None
    deleted: bool

    class Config:
        """config"""
        orm_mode = True


class CaptchaFileSchema(BaseModel):
    """CaptchaFileSchema"""
    id: int
    record_id: int
    filename: str
    file_type: str
    storage_id: int
    file_mark: str

    class Config:
        """config"""
        orm_mode = True
