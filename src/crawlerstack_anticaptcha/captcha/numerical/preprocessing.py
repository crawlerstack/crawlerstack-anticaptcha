"""Preprocessing"""
import logging
import os
from pathlib import Path

import cv2
import numpy as np

from crawlerstack_anticaptcha.config import settings


def take_first(elem):
    """take second"""
    return elem[0][0]


class Preprocessing:
    """preprocessing"""
    save_path = Path(settings.IMAGE_SAVE_PATH)

    def __init__(self, image: Path):
        self.img = str(image.resolve())
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @property
    def image(self):
        """
        对图像转灰度读取
        :return:
        """
        _img = cv2.imread(self.img, 0)
        return _img

    def blur(self):
        """
        降噪，
        :return:
        """
        blur = cv2.medianBlur(self.image, 3)
        return blur

    def inv(self):
        """
        第二次二值化
        :return:
        """
        _ret, thresh = cv2.threshold(self.blur(), 150, 255, cv2.THRESH_BINARY)

        return thresh

    def contours(self):
        """
        提取轮廓
        :return:
        """
        contours, _hierarchy = cv2.findContours(self.inv(), 2, 2)
        return contours

    def crop_image(self):
        """crop image"""
        result = []
        _contours = self.contours()
        _w = []
        for _ in _contours:
            x, y, w, h = cv2.boundingRect(_)
            _w.append(w)
        w_max = max(_w)
        for contour in _contours:
            x, y, w, h = cv2.boundingRect(contour)
            if x != 0 and y != 0 and w * h >= 75 and w < w_max:
                box = np.int0([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
                result.append(box)
            else:
                self.logger.debug('Image split failed.')
        result.sort(key=take_first)
        return result

    def save_single_image(self):
        """Save single image"""
        tag = 1
        img_list = self.crop_image()
        for box in img_list:
            cv2.drawContours(self.image, [box], 0, (0, 0, 255), 2)
            roi = self.inv()[box[0][1]:box[3][1], box[0][0]:box[1][0]]
            resize_img = cv2.resize(roi, (23, 19))
            filepath = self.save_path / f'numerical_captcha/char/{tag}.jpg'
            if not filepath.parent.exists():
                os.makedirs(filepath.parent)
                cv2.imwrite(str(filepath.resolve()), resize_img)
            else:
                cv2.imwrite(str(filepath.resolve()), resize_img)
            tag += 1

    @staticmethod
    def show_img(image):
        """
        show image
        :param image:
        :return:
        """
        cv2.imshow('img', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
