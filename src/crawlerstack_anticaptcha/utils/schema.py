"""Schema"""

from pydantic import BaseModel  # pylint:disable=no-name-in-module


class MessageData(BaseModel):
    """MessageData"""
    file_id: str
    value: int | str
    category: str


class Message(BaseModel):
    """Message"""
    code: int
    data: MessageData | None = None
    message: str


class RecordItem(BaseModel):
    """RecordingItem"""
    category: str
    success: bool
