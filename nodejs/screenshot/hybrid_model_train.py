"""
Train discriminative model to identify phishing site
base on pre-trained model, with the hybrid of the site url
"""

import numpy as np

# 随机种子，为了在不同时间跑出来的结果一致，可以去掉
np.random.seed(2018)

from keras.applications import VGG16, VGG19
from keras.layers import Input, Dense, concatenate
from keras.models import Model
from keras import optimizers
from keras import callbacks

from utils import *

def get_model(Base, url_input=True):
    """使用预训练模型参数构建训练网络

    Params:
        Base: `function` to get the base model such as VGG16, VGG19 etc.
        url_input: `boolean` whether embed url info to network

    Return:
        model architecture
    """
    input_layer = Input(shape=(None, None, 3), name='img_input')
    base_model = Base(input_tensor=input_layer, weights='imagenet', include_top=False, pooling='avg')

    x = base_model.output
    url_layer = Input(shape=(32,), name='url_input')

    if url_input is True:
        x = concatenate([x, url_layer])

    x = Dense(256, activation='relu')(x)
    prediction = Dense(2, activation='softmax')(x)

    if url_input is True:
        model = Model(inputs=[input_layer, url_layer], outputs=prediction)
    else:
        model = Model(inputs=input_layer, outputs=prediction)

    return model


def data_gen():
    large_train_dir = '/home/zgzhong/Desktop/phishing_sample/train'
    large_validate_dir = '/home/zgzhong/Desktop/phishing_sample/validate'

    data_generator = ImageUrlDataGenerator(rescale=1. / 255)

    large_train_data_gen = data_generator.flow_from_directory(
        directory=large_train_dir,
        json_path='picture.json',
        class_mode='categorical',
        batch_size=2
    )

    yield next(large_train_data_gen)

def img_gen():
    large_train_dir = '/home/zgzhong/Desktop/phishing_sample/train'
    data_generator = ImageUrlDataGenerator(rescale=1. / 255)

    large_train_data_gen = data_generator.flow_from_directory(
        directory=large_train_dir,
        class_mode='categorical',
        batch_size=2
    )

    yield next(large_train_data_gen)


# 设置优化函数
learning_rate = 0.003
adam_opt = optimizers.Adam(lr=learning_rate)
sgd_opt = optimizers.SGD(lr=learning_rate)

model = get_model(VGG16, url_input=True)
model.compile(optimizer=sgd_opt, loss='binary_crossentropy', metrics=['accuracy'])

# save best model
checkpoint = callbacks.ModelCheckpoint('phishing_weights_best.h5', monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callback_list = [checkpoint]

model.fit_generator()
print(model.predict_generator(data_gen(), steps=1, verbose=1))