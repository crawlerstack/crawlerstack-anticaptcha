"""train"""
import logging
from pathlib import Path

import cv2
import joblib
from sklearn.svm import SVC

clf = joblib.load(Path(__file__).parent.parent / 'models' / 'numerical_captcha.pkl')


class NumericalModel:
    """NumericalModel"""
    model_path = Path(__file__).parent.parent / 'models'

    def __init__(self, image_path: Path):
        self.image_path = image_path
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def extract(self):
        """Extract features"""
        samples = []
        labels = []
        for category_dir in self.image_path.iterdir():
            if category_dir.is_dir():
                for file in category_dir.iterdir():
                    img = cv2.imread(str(file.resolve()), 0)
                    res = cv2.resize(img, (23, 19))
                    res = res.reshape(23 * 19)
                    res_list = res.tolist()
                    samples.append(res_list)
                    labels.append(category_dir.name)
        return samples, labels

    def train(self):
        """train"""
        features = self.extract()
        letter_svm = SVC(kernel="linear", C=1).fit(features[0], features[1])
        joblib.dump(letter_svm, self.model_path / 'numerical_captcha.pkl')

    def identify(self):
        """identify"""
        captcha = []
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
