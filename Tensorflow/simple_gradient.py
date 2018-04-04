"""
simple gradient descent
"""
from __future__ import absolute_import, division, print_function
import tensorflow as tf
import tensorflow.contrib.eager as tfe

tf.enable_eager_execution()

NUM_EXAMPLES = 1000
training_inputs = tf.random_normal([NUM_EXAMPLES])
noise = tf.random_normal([NUM_EXAMPLES])
training_outputs = training_inputs * 3 + 2 + noise


def prediction(inputs, weight, bias):
    return inputs * weight + bias

# A loss fucntion using mean-squared error
def loss(weights, biases):
    error = prediction(training_inputs, weights, biases) -training_outputs
    return tf.reduce_mean(tf.square(error))

# Return the derivative of loss with respect to weight and bias
def grad(weights, biases):
    with tfe.GradientTape() as tape:
        loss_value = loss(weights, biases)
    return tape.gradient(loss_value, [weights, biases])


train_steps = 200
lr = 0.01

# Start with arbitrary value for W and B on the same batch of data
W = tfe.Variable(5.)
B = tfe.Variable(10.)

print("Initial loss: {:3f}".format(loss(W,B)))

for i in range(train_steps):
    dW, dB = grad(W, B)
    W.assign_sub(dW * lr)
    B.assign_sub(dB * lr)

    if i % 20 == 0:
        print("Loss at step {:03d}: {:.3f}".format(i, loss(W,B)))

print("Final loss: {:.3f}".format(loss(W, B)))
print("W={}, B={}".format(W.numpy(), B.numpy()))
