"""Utils"""
from enum import Enum
from pathlib import Path

from crawlerstack_anticaptcha.config import settings


class SliderCategory(Enum):
    """SliderCaptcha"""
    ID: int = 1
    CATEGORY: str = 'SliderCaptcha'
    SAVE_PATH: Path = Path(f'{settings.IMAGE_SAVE_PATH}').joinpath(Path('slider-captcha'))


class RotatedCategory(Enum):
    """RotatedCaptcha"""
    ID: int = 2
    CATEGORY: str = 'RotatedCaptcha'
    SAVE_PATH: Path = Path(f'{settings.IMAGE_SAVE_PATH}').joinpath(Path('rotated-captcha'))
