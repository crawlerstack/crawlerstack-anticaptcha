"""Schema"""

from pydantic import BaseModel  # pylint:disable=E0611


class MessageData(BaseModel):
    """MessageData"""
    file_id: str
    value: int | str
    category: str


class Message(BaseModel):
    """Message"""
    code: int
    data: MessageData | None
    message: str


class RecordItem(BaseModel):
    """RecordingItem"""
    category: str
    success: bool
