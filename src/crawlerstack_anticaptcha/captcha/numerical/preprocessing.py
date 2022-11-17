"""Preprocessing"""
import os

import cv2
import numpy as np

from crawlerstack_anticaptcha.utils.base_image import BasePreprocessing


def take_first(elem):
    """take second"""
    return elem[0][0]


class Preprocessing(BasePreprocessing):
    """preprocessing"""

    def blur(self):
        """
        降噪，
        :return:
        """
        blur = cv2.medianBlur(self.bg_image(), 3)
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
            cv2.drawContours(self.bg_image(), [box], 0, (0, 0, 255), 2)
            roi = self.inv()[box[0][1]:box[3][1], box[0][0]:box[1][0]]
            resize_img = cv2.resize(roi, (23, 19))
            filepath = self.captcha_image_path / f'numerical-captcha/split/{tag}.jpg'
            if not filepath.parent.exists():
                os.makedirs(filepath.parent)
                cv2.imwrite(str(filepath.resolve()), resize_img)
            else:
                cv2.imwrite(str(filepath.resolve()), resize_img)
            tag += 1
