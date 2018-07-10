#!/usr/bin/python

import tensorflow as tf
import tensorlayer as tl
from tensorlayer.layers import Layer


class Relu(Layer):
    def __init__(self, prev_layer, name):
        super(Relu, self).__init__(layer=prev_layer, name=name)
        self.inputs = prev_layer.outputs
        with tf.variable_scope(name):
            self.outputs = tf.nn.relu(self.inputs, name='relu_act')
        self.all_layers.append(self.outputs)


def entry_flow(x):
    def residual_block(x, block_idx, channel_num):
        prefix = 'block' + str(block_idx)
        residual = tl.layers.Conv2d(x, channel_num, (1, 1), (2, 2), padding='SAME', b_init=None, name=prefix+'_residual')
        residual = tl.layers.BatchNormLayer(residual, name=prefix+'_residual1_bn')
        x = tl.layers.SeparableConv2d(x, channel_num, (3, 3), padding='SAME', b_init=None, name=prefix+'_sepconv1')
        x = tl.layers.BatchNormLayer(x, name=prefix+'_sepconv1_bn', act=tf.nn.relu)
        x = tl.layers.SeparableConv2d(x, channel_num, (3, 3), padding='SAME', b_init=None, name=prefix+'_sepconv2')
        x = tl.layers.BatchNormLayer(x, name=prefix+'_sepconv2_bn', act=tf.nn.relu)
        x = tl.layers.MaxPool2d(x, (3, 3), padding='SAME', name=prefix+'_max_pool')
        x = tl.layers.ElementwiseLayer([x, residual], tf.add, name=prefix+'_residual_add')
        return x

    net = tl.layers.Conv2d(x, 32, (3, 3), (2, 2), padding='VALID', b_init=None, name='block1_conv1')
    net = tl.layers.BatchNormLayer(net, name='block1_conv1_bn', act=tf.nn.relu)
    net = tl.layers.Conv2d(net, 64, (3, 3), padding='VALID', b_init=None, name='block1_conv2')
    net = tl.layers.BatchNormLayer(net, name='block1_conv2_bn', act=tf.nn.relu)

    net = residual_block(net, block_idx=2, channel_num=128)
    net = residual_block(net, block_idx=3, channel_num=256)
    net = residual_block(net, block_idx=4, channel_num=728)

    return net

def middle_flow(net):
    def residual_block(x, block_idx):
        residual = x

        prefix = 'block' + str(block_idx)
        x = Relu(x, name=prefix+'_sepconv1_act')
        x = tl.layers.SeparableConv2d(x, 728, (3, 3), padding='SAME', b_init=None, name=prefix+'_sepconv1')
        x = tl.layers.BatchNormLayer(x, name=prefix+'_sepconv1_bn')

        x = Relu(x, name=prefix+'_sepconv2_act')
        x = tl.layers.SeparableConv2d(x, 728, (3, 3), padding='SAME', b_init=None, name=prefix+'_sepconv2')
        x = tl.layers.BatchNormLayer(x, name=prefix+'_sepconv2_bn')

        x = Relu(x, name=prefix+'_sepconv3_act')
        x = tl.layers.SeparableConv2d(x, 728, (3, 3), padding='SAME', b_init=None, name=prefix+'_sepconv3')
        x = tl.layers.BatchNormLayer(x, name=prefix+'_sepconv3_bn')

        x = tl.layers.ElementwiseLayer([x, residual], tf.add, name=prefix+'_residual_add')
        return x

    for i in range(8):
        net = residual_block(net, i+5)

    return net


def exit_flow(x):
    residual = tl.layers.Conv2d(x, 1024, (1, 1), (2, 2), padding='SAME', b_init=None, name='block13_residual')

    x = Relu(x, name='block13_sepconv1_act')
    x = tl.layers.SeparableConv2d(x, 728, (3,3), padding='SAME', b_init=None, name='block13_sepconv1')
    x = tl.layers.BatchNormLayer(x, name='block13_sepconv1_bn', act=tf.nn.relu)
    x = tl.layers.SeparableConv2d(x, 1024, (3, 3), padding='SAME', b_init=None, name='block12_sepocnv2')
    x = tl.layers.BatchNormLayer(x, name='block13_sepconv2_bn')
    x = tl.layers.MaxPool2d(x, (3, 3), (2, 2), padding='SAME', name='block13_pool')
    x = tl.layers.ElementwiseLayer([x, residual], tf.add, name='block13_residual_add')

    x = tl.layers.SeparableConv2d(x, 1536, (3, 3), padding='SAME', b_init=None, name='block14_sepconv1')
    x = tl.layers.BatchNormLayer(x, name='block14_sepconv1_bn', act=tf.nn.relu)
    x = tl.layers.SeparableConv2d(x, 2048, (3, 3), padding='SAME', b_init=None, name='block14_sepconv2')
    x = tl.layers.BatchNormLayer(x, name='block14_sepconv2_bn', act=tf.nn.relu)

    return x

def Xception(input):
    img_input = tl.layers.InputLayer(input, name='Input')
    net = entry_flow(img_input)
    net = middle_flow(net)
    net = exit_flow(net)

    return net


if __name__ == '__main__':
    sess = tf.InteractiveSession()
    x = tf.placeholder(tf.float32, shape=(None, 299, 299, 3), name='x')
    net = Xception(x)


    tl.layers.initialize_global_variables(sess)
    net.print_params()
    net.print_layers()

    sess.close()

