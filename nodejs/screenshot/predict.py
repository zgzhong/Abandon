import numpy as np
import cv2
import keras
import os
import glob
import json
from urllib.parse import urlsplit
from keras.preprocessing.text import hashing_trick


class Classfier(object):
    def __init__(self, model_path):
        self._model_path = model_path
        self._model = None

        self.setup()

    def setup(self):
        raise NotImplementedError

class PhishingClassfier(Classfier):
    def setup(self):
        self._model = keras.models.load_model(self._model_path)
        self._input_shape = 256, 256

    @staticmethod
    def gen_url_info(*urls):
        n = 1024 * 1024 * 10
        info_array = np.empty(shape=(1, 0))  # empty array

        for raw_url in urls:
            # generate specify string for hash
            url = urlsplit(raw_url)
            port = url.port or 80
            if url.scheme == 'https':
                port = 443
            val = '{scheme}/{netloc}/{port}{path}'.format(scheme=url.scheme, netloc=url.netloc, port=port, path=url.path)

            # compute hash array
            hash_val = hashing_trick(val, n, hash_function='md5', filters='', split='/')[:16]
            # padding the hash_val with 0 whose length is smaller than 16
            hash_val = np.pad(hash_val, (0, 16 - len(hash_val)), mode='constant', constant_values=0)[np.newaxis]
            info_array = np.c_[info_array, hash_val]

        return info_array / n

    def judge(self, img, origin_url, landed_url):
        """Determine whether the image is from phishing website

        Params:
            img: `np.ndarray` image pixel array
            origin_url: `str`
            landed_url: `str`
        Return:
            determined class of the img and its score
        """
        url_info = self.gen_url_info(origin_url, landed_url)
        img = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), self._input_shape).astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        out = self._model.predict([img, url_info])

        is_phishing = np.argmax(out)
        score = out[0][is_phishing]
        return is_phishing, score


def main():
    """test the predict function"""
    def load_json(path):
        url_map = {}

        with open(path) as f:
            json_list = json.load(f)

        for item in json_list:
            if item['status'] == 'failed':
                continue
            origin_val = item['origin_url']
            landed_val = item['landed_url']

            key = os.path.basename(item['fname'])
            url_map[key] = [origin_val, landed_val]

        return url_map

    predictor = PhishingClassfier(model_path='phishing_model_vgg16_large_withurl.h5')
    predict_files = glob.glob('picture/*.jpg')
    url_map = load_json('result.json')

    for fname in predict_files:
        img = cv2.imread(fname, flags=cv2.IMREAD_COLOR)
        result, score = predictor.judge(img, *url_map[os.path.basename(fname)])

        print(fname, result, score)


if __name__ == '__main__':
    main()


