import cv2

import numpy as np

from keras.models import load_model
from utils import *


def predict(model, site_detail, img_path=None):
    if not isinstance(site_detail, dict):
        raise ValueError('params site_detail must be dict')

    im_data = load_img(img_path, cv2.IMREAD_COLOR) / 255.
    if im_data is None:
        raise ValueError('img_path cant\'nt both be None')

    url_data = get_url_info(site_detail, fname=img_path)

    im_data = np.expand_dims(im_data, axis=0)
    url_data = np.expand_dims(url_data, axis=0)

    result = model.predict([im_data, url_data])
    return result


model = load_model('phishing_url_vgg19_best.h5')

