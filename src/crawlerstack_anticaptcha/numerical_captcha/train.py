"""train"""
import logging
import os
import time
from pathlib import Path, PurePath

import cv2
import joblib
import requests
from sklearn.svm import SVC

from crawlerstack_anticaptcha.config import settings

train_images_path = Path('/tmp/download_image/train')
test_path = Path("/tmp/download_image/part/test")
model_path = Path('../captcha_models/numerical_captcha.pkl')
train_set_x = []
train_set_y = []


class NumericalModel:
    """NumericalModel"""
    train_images_path = Path(settings.IMAGE_SAVE_PATH) / 'numerical-captcha/train'
    test_path = Path(settings.IMAGE_SAVE_PATH) / 'numerical-captcha/test'
    model_path = Path('../captcha_models')

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    @staticmethod
    def create_captcha():
        """create_captcha"""
        session = requests.Session()
        for _num in range(10):
            img_url = 'http://run.hbut.edu.cn/Account/GetValidateCode?time=1644928431690'
            print(img_url)
            res = session.get(img_url)
            timestamp = int(round(time.time() * 1000))
            file = PurePath(settings.IMAGE_SAVE_PATH) / f"numerical-captcha/train/{timestamp}.jpg"
            try:
                with open(file, "ab") as f:
                    f.write(res.content)
            except FileNotFoundError:
                os.makedirs(file.parent)
                with open(file, "ab") as f:
                    f.write(res.content)

    def train(self):
        """train"""
        for category in self.train_images_path.iterdir():
            if category.is_file():
                continue
            for file in category.iterdir():
                img = cv2.imread(str(file.resolve()), 0)
                res = cv2.resize(img, (14, 10))
                res_1 = res.reshape(140)
                res_list = res_1.tolist()
                train_set_x.append(res_list)
                train_set_y.append(category.name)
            letter_svm = SVC(kernel="linear", C=1).fit(train_set_x, train_set_y)
            joblib.dump(letter_svm, self.model_path / 'numerical_captcha.pkl')

    def verify(self):
        """verify"""
        captcha = []
        clf = joblib.load(model_path / 'numerical_captcha.pkl')
        for i in self.test_path.iterdir():
            img = cv2.imread(str(i.resolve()), 0)
            img_resize = cv2.resize(img, (14, 10))
            data = img_resize.reshape(140)
            data = data.reshape(1, -1)
            num = clf.predict(data)[0]
            captcha.append(num)
        captcha = ','.join(map(str, captcha))
        self.logger.info('The captcha result is %s', captcha)
