"""Message"""
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
