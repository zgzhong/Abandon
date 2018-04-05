import tensorflow as tf
import tensorflow.contrib.eager as tfe
import dataset

tf.enable_eager_execution()


# inheriting from `tf.keras.Model`
class MNISTModel(tf.keras.Model):
    def __init__(self):
        super(MNISTModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(units=10)
        self.dense2 = tf.keras.layers.Dense(units=10)

    def call(self, input):
        """Run the model."""
        result = self.dense1(input)
        result = self.dense2(result)
        result = self.dense2(result)  # resue variables from dense2 layer
        return result

model = MNISTModel()

dataset_train = dataset.train('./datasets').shuffle(60000).repeat(4).batch(32)

def loss(model, x, y):
    prediction = model(x)
    return tf.losses.sparse_softmax_cross_entropy(labels=y, logits=prediction)

def grad(model, inputs, targets):
    with tfe.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, model.variables)

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)

x, y  = tfe.Iterator(dataset_train).next()
print("Initial loss: {:.3f}".format(loss(model, x, y)))


# training loop
for (i, (x,y)) in enumerate(tfe.Iterator(dataset_train)):
    # Calculate derivatives of the input function with respect to its parameters
    grads = grad(model, x, y)
    # Apply the gradient to the model
    optimizer.apply_gradients(zip(grads, model.variables),
                              global_step=tf.train.get_or_create_global_step())
    if i % 200 == 0:
        print("Loss at step {:04d}: {:.3f}".format(i, loss(model, x, y)))
        print(grads)

print("Final loss: {:.3f}".format(loss(model, x, y)))

