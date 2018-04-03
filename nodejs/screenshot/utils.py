import os
import cv2
import json
import numpy as np
import keras.backend as K

from functools import partial
from urllib.parse import urlsplit
from keras.preprocessing import text
from keras.preprocessing import image


def load_img(img_path, img_mode, max_size=512.):
    img = cv2.imread(img_path, img_mode)  # channel last
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    w = img.shape[0]
    h = img.shape[1]
    maxl = max(w, h)
    scale = 1
    if maxl > max_size:
        scale = max_size / maxl

    ws = int(np.ceil(w * scale))
    hs = int(np.ceil(h * scale))
    im_data = cv2.resize(img, dsize=(hs, ws))
    return im_data


def load_json(json_path):
    with open(json_path) as f:
        json_list = json.load(f)

    url_map = {}

    for item in json_list:
        if item['status'] == 'failed':
            continue
        origin_val = item['origin_url']
        landed_val = item['landed_url']

        key = os.path.basename(item['fname'])
        url_map[key] = [origin_val, landed_val]

    return url_map


def get_url_info(url_map, fname):
    n = 1024 * 1024 * 10
    info_array = np.array([]).astype(np.float32)  # emtpy array

    key = os.path.basename(fname)
    urls = url_map[key]

    for raw_url in urls:
        url = urlsplit(raw_url)
        port = url.port or 80
        if url.scheme == 'https':
            port = 443
        val = '{scheme}/{netloc}/{port}{path}{query}'.format(
            scheme=url.scheme,
            netloc=url.netloc,
            port=port,
            path=url.path,
            query=url.query
        )
        hash_val = text.hashing_trick(val, n, hash_function='md5', filters='/&', split=' ')[:16]
        hash_val = np.pad(hash_val, (0, 16 - len(hash_val)), mode='constant', constant_values=0)

        info_array = np.r_[info_array, hash_val]

    return info_array / n


def mask_image(img, x, y, w, h):
    """mask some img region to zero"""

    mask = np.ones(img.shape[:2], np.uint8) * 255
    mask[y:y+h, x:x+w] = 0
    return cv2.bitwise_and(img, img, mask=mask)


class ImageUrlDataGenerator(image.ImageDataGenerator):
    def flow_from_directory(self, directory, *args, **kwargs):
        return ImageUrlDataIterator(directory, self, *args, **kwargs)


class ImageUrlDataIterator(image.DirectoryIterator):
    def __init__(self, *args, json_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.embed_url = json_path is not None

        if self.embed_url:
            url_map = load_json(json_path)
            self._get_url_info = partial(get_url_info, url_map=url_map)

    def _get_batches_of_embed_url_samples(self, index_array):
        img_mode = cv2.IMREAD_COLOR
        if self.color_mode == 'grayscale':
            img_mode = cv2.IMREAD_GRAYSCALE

        # build batch of data
        batch_img = []
        batch_url = []

        for fname in (self.filenames[i] for i in index_array):
            img_data = load_img(os.path.join(self.directory, fname), img_mode).astype(np.float32)
            img_data = self.image_data_generator.random_transform(img_data)
            img_data = self.image_data_generator.standardize(img_data)
            url_data = self._get_url_info(fname=fname)

            batch_img.append(img_data)
            batch_url.append(url_data)

        batch_img = np.array(batch_img)
        batch_url = np.array(batch_url)

        # build batch of labels
        if self.class_mode == 'input':
            raise ValueError('ImageUrlDataIterator does not support `class_mode`: input')
        elif self.class_mode == 'sparse':
            batch_y = self.classes[index_array]
        elif self.class_mode == 'binary':
            batch_y = self.classes[index_array].astype(K.floatx())
        elif self.class_mode == 'categorical':
            batch_y = np.zeros((len(index_array), self.num_classes), dtype=K.floatx())
            for i, label in enumerate(self.classes[index_array]):
                batch_y[i, label] = 1.
        else:
            return [batch_img, batch_url]

        return [batch_img, batch_url], batch_y

    def _get_batches_of_image_samples(self, index_array):
        img_mode = cv2.IMREAD_COLOR
        if self.color_mode == 'grayscale':
            img_mode = cv2.IMREAD_GRAYSCALE

        batch_x = []
        for fname in (self.filenames[i] for i in index_array):
            img_data = load_img(os.path.join(self.directory, fname), img_mode).astype(np.float32)
            img_data = self.image_data_generator.random_transform(img_data)
            img_data = self.image_data_generator.standardize(img_data)

            batch_x.append(img_data)

        batch_x = np.array(batch_x)

        # build batch of labels
        if self.class_mode == 'input':
            raise ValueError('ImageUrlDataIterator does not support `class_mode`: input')
        elif self.class_mode == 'sparse':
            batch_y = self.classes[index_array]
        elif self.class_mode == 'binary':
            batch_y = self.classes[index_array].astype(K.floatx())
        elif self.class_mode == 'categorical':
            batch_y = np.zeros((len(batch_x), self.num_classes), dtype=K.floatx())
            for i, label in enumerate(self.classes[index_array]):
                batch_y[i, label] = 1.
        else:
            return batch_x

        return batch_x, batch_y

    def next(self):
        """For python 2.x

        # Returns
            The next batch
        """
        with self.lock:
            index_array = next(self.index_generator)

        # The transformation of images is not under thread lock
        # so it can be done in parallel
        if self.embed_url:
            return self._get_batches_of_embed_url_samples(index_array)
        else:
            return self._get_batches_of_image_samples(index_array)
