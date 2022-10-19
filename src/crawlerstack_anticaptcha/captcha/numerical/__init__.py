"""DdddOcr"""
import base64
import io
import json
import os
import pathlib

import numpy as np
import onnxruntime
from PIL import Image


def base64_to_image(img_base64):
    """
    base64_to_image
    :param img_base64:
    :return:
    """
    img_data = base64.b64decode(img_base64)
    return Image.open(io.BytesIO(img_data))


class DdddOcr(object):
    """DdddOcr"""

    model_path = pathlib.Path(__file__).parent.parent / 'models'

    def __init__(self, ocr: bool = True, det: bool = False, beta: bool = False,
                 use_gpu: bool = False,
                 device_id: int = 0, import_onnx_path: str = "", charsets_path: str = ""):
        self.det = False
        self.use_import_onnx = False
        self.__word = False
        self.__resize = []
        self.__channel = 1
        self.graph_path = os.path.join(self.model_path, 'common.onnx')
        if import_onnx_path != "":
            det = False
            ocr = False
            self.__graph_path = import_onnx_path
            with open(charsets_path, 'r', encoding="utf-8") as f:
                info = json.loads(f.read())
            self.__charset = info['charset']
            self.__word = info['word']
            self.__resize = info['image']
            self.__channel = info['channel']
            self.use_import_onnx = True

        if det:
            ocr = False
            self.graph_path = os.path.join(self.model_path, 'common_det.onnx')
            self.__charset = []
        if ocr:
            if not beta:
                self.graph_path = os.path.join(self.model_path, 'common_old.onnx')
                self.__charset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            else:
                self.graph_path = os.path.join(self.model_path, 'common.onnx')
                self.__charset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if use_gpu:
            self.providers = [
                ('CUDAExecutionProvider', {
                    'device_id': device_id,
                    'arena_extend_strategy': 'kNextPowerOfTwo',
                    'cuda_mem_limit': 2 * 1024 * 1024 * 1024,
                    'cudnn_conv_algo_search': 'EXHAUSTIVE',
                    'do_copy_in_default_stream': True,
                }),
            ]
        else:
            self.providers = [
                'CPUExecutionProvider',
            ]
        if ocr or det or self.use_import_onnx:
            self.__ort_session = onnxruntime.InferenceSession(self.graph_path, providers=self.providers)

    def classification(self, img):
        """classification"""
        if self.det:
            raise TypeError("当前识别类型为目标检测")
        if not isinstance(img, (bytes, str, pathlib.PurePath, Image.Image)):
            raise TypeError("未知图片类型")
        if isinstance(img, bytes):
            image = Image.open(io.BytesIO(img))
        elif isinstance(img, Image.Image):
            image = img.copy()
        elif isinstance(img, str):
            image = base64_to_image(img)
        else:
            assert isinstance(img, pathlib.PurePath)
            image = Image.open(img)
        if not self.use_import_onnx:
            image = image.resize((int(image.size[0] * (64 / image.size[1])), 64), Image.ANTIALIAS).convert('L')
        else:
            if self.__resize[0] == -1:
                if self.__word:
                    image = image.resize((self.__resize[1], self.__resize[1]), Image.ANTIALIAS)
                else:
                    image = image.resize((int(image.size[0] * (self.__resize[1] / image.size[1])), self.__resize[1]),
                                         Image.ANTIALIAS)
            else:
                image = image.resize((self.__resize[0], self.__resize[1]), Image.ANTIALIAS)
            if self.__channel == 1:
                image = image.convert('L')
            else:
                image = image.convert('RGB')
        image = np.array(image).astype(np.float32)
        image = np.expand_dims(image, axis=0) / 255.
        if not self.use_import_onnx:
            image = (image - 0.5) / 0.5
        else:
            if self.__channel == 1:
                image = (image - 0.456) / 0.224
            else:
                image = (image - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
                image = image[0]
                image = image.transpose((2, 0, 1))

        ort_inputs = {'input1': np.array([image]).astype(np.float32)}
        ort_outs = self.__ort_session.run(None, ort_inputs)
        result = []

        last_item = 0
        if self.__word:
            for item in ort_outs[1]:
                result.append(self.__charset[item])
        else:
            for item in ort_outs[0][0]:
                if item == last_item:
                    continue
                else:
                    last_item = item
                if item != 0:
                    result.append(self.__charset[item])

        return ''.join(result)
