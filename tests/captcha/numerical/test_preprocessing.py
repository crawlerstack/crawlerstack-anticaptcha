"""test preprocessing"""
import cv2

from crawlerstack_anticaptcha.captcha.numerical.preprocessing import (
    Preprocessing, take_first)


def test_take_first():
    """test take first"""
    result = take_first([[1, 2, 3], [4, 5, 6]])
    assert result == 1


def test_blur(mocker):
    """test blur"""
    preprocessing = Preprocessing(mocker.MagicMock())
    mocker.patch.object(cv2, 'medianBlur', return_value=1)
    assert preprocessing.blur() == 1


def test_inv(mocker):
    """test inv"""
    preprocessing = Preprocessing(mocker.MagicMock())
    mocker.patch.object(Preprocessing, 'blur', return_value=1)
    mocker.patch.object(cv2, 'threshold', return_value=(1, 2))
    assert preprocessing.inv() == 2


def test_contours(mocker):
    """test contours"""
    preprocessing = Preprocessing(mocker.MagicMock())
    mocker.patch.object(Preprocessing, 'inv', return_value=1)
    mocker.patch.object(cv2, 'findContours', return_value=(1, 2))
    assert preprocessing.contours() == 1
