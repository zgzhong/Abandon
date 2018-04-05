"""
这个脚本计算了目标损失函数 f(x) = x^2 的全局最小值(刚好有全局最小)
"""
import tensorflow as tf
import tensorflow.contrib.eager as tfe
tf.enable_eager_execution()

w = tfe.Variable([[1.]])
lr = 0.01
for _ in range(100):
    with tfe.GradientTape() as tape:
        loss = w *  w
    dw, = tape.gradient(loss, [w])
    w.assign_sub(dw * lr)
print("w={}".format(w.numpy()))
