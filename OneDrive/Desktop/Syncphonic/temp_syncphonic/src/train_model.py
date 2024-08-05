import os
import sys
import tensorflow as tf
import numpy as np
from scipy.sparse import csr_matrix
import random
from matplotlib import pyplot as plt
import time

# Set environment variables
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_MLIR_ENABLE_V1_COMPILER'] = '1'

# Ensure the parent directory is in the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.model_definition import create_weights, create_biases, conv_layer, flatten_layer, dense_layer, rnn_cell

# Check TensorFlow version
print("TensorFlow Version:", tf.__version__)

# Ensure compatibility with TensorFlow 1.x code
if tf.__version__.startswith('2'):
    tf.compat.v1.disable_eager_execution()

def train_model(train, train_captions, vocab_size, fwd_dict, size=(256, 256), num_channels=3, learning_rate=0.0001, training_iters=2, display_step=1, batch_size=2):
    max_sent_limit = 50
    bridge_size = 256  # Reduced bridge size

    x_caption = tf.compat.v1.placeholder(tf.float32, [None, vocab_size], name='x_caption')
    x_inp = tf.compat.v1.placeholder(tf.float32, shape=[None, size[0], size[1], num_channels], name='x_image')
    y = tf.compat.v1.placeholder(tf.float32, [None, vocab_size], name='y')

    Wconv = tf.Variable(tf.random.truncated_normal([bridge_size, vocab_size], stddev=0.7))
    bconv = tf.Variable(tf.zeros([1, vocab_size]))
    Wi = tf.Variable(tf.random.truncated_normal([vocab_size, vocab_size], stddev=0.7))
    Wf = tf.Variable(tf.random.truncated_normal([vocab_size, vocab_size], stddev=0.7))
    Wo = tf.Variable(tf.random.truncated_normal([vocab_size, vocab_size], stddev=0.7))
    b = tf.Variable(tf.zeros([1, vocab_size]))

    # Further reduced number of convolutional layers and kernels
    layer_conv1 = conv_layer(inp=x_inp, kernel_shape=(3, 3), num_kernels=8, num_channels=3, suffix='1')
    maxpool1 = tf.nn.max_pool2d(layer_conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    flat_layer = flatten_layer(maxpool1, suffix='2')

    # Calculate the correct size after flattening
    flattened_size = 8 * (size[0] // 2) * (size[1] // 2)  # One max-pooling layer halving the dimensions

    dense_layer_1 = dense_layer(inp=flat_layer, num_inputs=flattened_size, num_outputs=bridge_size, suffix='3')  # Adjusted num_inputs
    h = dense_layer_1

    start_tag = '<s>'
    end_tag = '<e>'
    if start_tag not in fwd_dict or end_tag not in fwd_dict:
        print(f"Error: Start token '{start_tag}' or end token '{end_tag}' not found in fwd_dict")
        return None

    start_hook = tf.cast(csr_matrix(([1], ([0], [fwd_dict[start_tag]])), shape=(1, vocab_size)).toarray(), tf.float32)
    end_hook = tf.cast(csr_matrix(([1], ([0], [fwd_dict[end_tag]])), shape=(1, vocab_size)).toarray(), tf.float32)
    hook = tf.slice(x_caption, [0, 0], [1, vocab_size])
    h, out = rnn_cell(Wi, Wo, Wconv, bconv, h, hook)

    def fn(prev, curr):
        h = prev[0]
        curr = tf.reshape(curr, [1, vocab_size])
        h, out = rnn_cell(Wi, Wo, Wf, b, h, curr)
        return h, out

    _, output = tf.scan(fn, x_caption[1:], initializer=(h, out))
    output = tf.squeeze(output, axis=1)
    outputs = tf.concat([out, output], axis=0)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=outputs, labels=y))
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(cost)
    pred = tf.nn.softmax(outputs)
    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    print("Starting TensorFlow session...")
    with tf.compat.v1.Session() as sess:
        sess.run(tf.compat.v1.global_variables_initializer())
        m = len(train_captions)
        print(f"Training data size: {m}")
        for epoch in range(training_iters):
            start_time = time.time()
            total_cost = 0
            total_acc = 0
            for i in range(0, min(m, 50), batch_size):  # Use only the first 50 samples
                end = i + batch_size
                batch_train = train[i:end]
                batch_train_captions = train_captions[i:end]
                for j in range(len(batch_train_captions)):
                    try:
                        x_caption_array = batch_train_captions[j][:-1].toarray()
                        y_array = batch_train_captions[j][1:].toarray()
                        if x_caption_array.shape[1] != vocab_size or y_array.shape[1] != vocab_size:
                            raise ValueError(f"Shape mismatch: x_caption_array shape {x_caption_array.shape}, y_array shape {y_array.shape}")

                        _, cst, acc = sess.run([optimizer, cost, accuracy], feed_dict={
                            x_caption: x_caption_array, 
                            x_inp: batch_train[j:j + 1], 
                            y: y_array
                        })
                        total_cost += cst
                        total_acc += acc
                    except Exception as e:
                        print(f"Error at epoch {epoch}, step {i}, batch {j}: {e}")
                        return
                print(f"Completed batch {i} to {end} of epoch {epoch}")
            end_time = time.time()
            epoch_duration = end_time - start_time
            print(f"Epoch {epoch + 1} completed in {epoch_duration:.2f} seconds")
            print(f'Epoch {epoch + 1}: Cost = {total_cost / min(m, 500):.4f}, Accuracy: {total_acc * 100 / min(m, 500):.2f}%')
        print('Optimization finished!')
        return sess

def predict_caption(sess, train, real_images, train_captions, vocab_size, rev_dict, num_tests=12):
    final_prediction = tf.squeeze(final_outputs.stack())  # Define final_outputs properly

    for tests in range(num_tests):
        image_num = random.randint(0, len(train) - 1)
        caption = sess.run(final_prediction, feed_dict={x_inp: train[image_num:image_num + 1]})
        caption = np.argmax(caption[:-1], 1)
        capt = ' '.join([rev_dict[i] for i in caption])
        print('Predicted Caption:->', capt)
        orig_cap = np.argmax(train_captions[image_num:image_num + 1][0][1:-1].toarray(), 1)
        original_caption = ' '.join([rev_dict[i] for i in orig_cap])
        plt.imshow(real_images[image_num])
        plt.title('Image')
        plt.show()

print("Loading dataset...")
# Assuming you have code to load `train`, `train_captions`, `vocab_size`, `fwd_dict`, `rev_dict`, `real_images`
# train, train_captions, vocab_size, fwd_dict, rev_dict, real_images = load_dataset()  # Implement this function

# Print to verify if dataset is loaded correctly
# print("Dataset loaded successfully.")

# Assuming the `train_model` and `predict_caption` functions are correctly defined, you can call them like this:
# sess = train_model(train, train_captions, vocab_size, fwd_dict)
# if sess:
#     predict_caption(sess, train, real_images, train_captions, vocab_size, rev_dict)
