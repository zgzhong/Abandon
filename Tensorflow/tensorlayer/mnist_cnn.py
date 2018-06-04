import tensorflow as tf
import tensorlayer as tl


def build_cnn(input):
    # define network
    network = tl.layers.InputLayer(input, name='input_layer')
    network = tl.layers.Conv2d(network, 16, (3, 3), (1, 1), padding='VALID', name='conv1', act=tf.nn.relu)
    network = tl.layers.MaxPool2d(network, (2, 2), (2, 2), padding='VALID', name='pool1')
    network = tl.layers.Conv2d(network, 16, (3, 3), (1, 1), padding='VALID', name='conv2', act=tf.nn.relu)
    network = tl.layers.MaxPool2d(network, (2, 2), (2, 2), padding='VALID', name='pool2')
    network = tl.layers.FlattenLayer(network, name='flatten')
    network = tl.layers.DenseLayer(network, n_units=10, name='dense2')
    return network


def build_sep_cnn(input):
    # define network
    network = tl.layers.InputLayer(input, name='input_layer')
    network = tl.layers.Conv2d(network, 8, (3, 3), (1, 1), padding='VALID', name='conv1')

    network = tl.layers.DepthwiseConv2d(network, (3, 3), (1, 1), padding='VALID', name='depth_conv1')
    network = tl.layers.BatchNormLayer(network, act=tf.nn.relu, is_train=True, name='bn11')
    network = tl.layers.Conv2d(network, 16, (1, 1), (1, 1),  padding='VALID', name='conv2')
    network = tl.layers.BatchNormLayer(network, act=tf.nn.relu, is_train=True ,name='bn12')

    network = tl.layers.MaxPool2d(network, (2, 2), (2, 2), padding='VALID', name='pool1')

    network = tl.layers.DepthwiseConv2d(network, (3, 3), (1, 1), padding='VALID', name='depth_conv2')
    network = tl.layers.BatchNormLayer(network, act=tf.nn.relu, is_train=True, name='bn21')
    network = tl.layers.Conv2d(network, 16, (1, 1), (1, 1), padding='VALID', name='conv3')
    network = tl.layers.BatchNormLayer(network, act=tf.nn.relu, is_train=True, name='bn22')

    network = tl.layers.MaxPool2d(network, (2, 2), (2, 2), padding='VALID', name='pool2')

    network = tl.layers.FlattenLayer(network, name='flatten')
    network = tl.layers.DenseLayer(network, n_units=10, name='dense2')
    return network


def train_model(network_f, model_name):
    X_train, y_train, X_val, y_val, X_test, y_test = tl.files.load_mnist_dataset(shape=(-1, 28, 28, 1))

    x = tf.placeholder(dtype=tf.float32, shape=(None, 28, 28, 1), name='x')
    y_ = tf.placeholder(dtype=tf.int64, shape=(None,), name='y_')

    network = network_f(x)
    y = network.outputs

    # define cost function and metric.
    cost = tl.cost.cross_entropy(y, y_, 'xentropy')
    correct_prediction = tf.equal(tf.argmax(y, 1), y_)
    acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    y_op = tf.argmax(tf.nn.softmax(y), 1)

    # define the optimizer
    train_params = network.all_params
    train_op = tf.train.AdamOptimizer(learning_rate=0.0001, beta1=0.9, beta2=0.999,
                                      epsilon=1e-08, use_locking=False).minimize(cost, var_list=train_params)


    sess = tf.Session()
    tl.layers.initialize_global_variables(sess)

    # print network information
    network.print_params(session=sess)
    network.print_layers()

    # train the network
    tl.utils.fit(sess, network, train_op, cost, X_train, y_train, x, y_,
                 acc=acc, batch_size=500, n_epoch=10, print_freq=5,
                 X_val=X_val, y_val=y_val, eval_train=False)

    # evaluation
    tl.utils.test(sess, network, acc, X_test, y_test, x, y_, batch_size=200, cost=cost)

    # save the network to .npz file
    tl.files.save_npz(network.all_params, name=model_name, sess=sess)
    sess.close()


if __name__ == '__main__':
    train_model(build_sep_cnn, 'model_sep_cnn.npz')
    train_model(build_cnn, 'model_cnn.npz')
