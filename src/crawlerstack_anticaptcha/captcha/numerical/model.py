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


def create_captcha():
    """create_captcha"""
    session = requests.Session()
    for _num in range(10):
        img_url = 'http://run.hbut.edu.cn/Account/GetValidateCode?time=1644928431690'
        print(img_url)
        res = session.get(img_url)
        timestamp = int(round(time.time() * 1000))
        file = PurePath(settings.IMAGE_SAVE_PATH) / f"numerical_captcha/{timestamp}.jpg"
        try:
            with open(file, "ab") as f:
                f.write(res.content)
        except FileNotFoundError:
            os.makedirs(file.parent)
            with open(file, "ab") as f:
                f.write(res.content)


class NumericalModel:
    """NumericalModel"""
    model_path = Path(__file__).parent.parent / 'models'

    def __init__(self, image_path: Path):
        self.image_path = image_path
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def train(self):
        """train"""
        samples = []
        labels = []
        for category_dir in self.image_path.iterdir():
            if category_dir.is_file():
                continue
            for file in category_dir.iterdir():
                img = cv2.imread(str(file.resolve()), 0)
                res = cv2.resize(img, (23, 19))
                res = res.reshape(23 * 19)
                res_list = res.tolist()
                samples.append(res_list)
                labels.append(category_dir.name)
        letter_svm = SVC(kernel="linear", C=1).fit(samples, labels)
        joblib.dump(letter_svm, self.model_path / 'numerical_captcha.pkl')

    def identify(self):
        """identify"""
        captcha = []
        clf = joblib.load(self.model_path / 'numerical_captcha.pkl')
        for i in self.image_path.iterdir():
            if not i.is_file():
                continue
            img = cv2.imread(str(i.resolve()), 0)
            img_resize = cv2.resize(img, (23, 19))
            data = img_resize.reshape(23 * 19)
            data = data.reshape(1, -1)
            num = clf.predict(data)[0]
            captcha.append(num)
        captcha = ''.join(map(str, captcha))
        self.logger.info('The model identification result is %s.', captcha)
        return captcha
