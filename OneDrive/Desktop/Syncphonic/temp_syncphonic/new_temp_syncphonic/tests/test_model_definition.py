import unittest
import tensorflow as tf
from src.model_definition import create_weights, create_biases, conv_layer, flatten_layer, dense_layer, rnn_cell

class TestModelDefinition(unittest.TestCase):
    
    def test_create_weights(self):
        weights = create_weights((3, 3), 'test')
        self.assertIsInstance(weights, tf.Variable)

    def test_create_biases(self):
        biases = create_biases(3, 'test')
        self.assertIsInstance(biases, tf.Variable)

    def test_conv_layer(self):
        inp = tf.placeholder(tf.float32, [1, 256, 256, 3])
        layer = conv_layer(inp, (3, 3), 3, 32, 'test')
        self.assertIsNotNone(layer)

    def test_flatten_layer(self):
        inp = tf.placeholder(tf.float32, [1, 256, 256, 3])
        flat_layer = flatten_layer(inp, 'test')
        self.assertIsNotNone(flat_layer)

    def test_dense_layer(self):
        inp = tf.placeholder(tf.float32, [1, 256])
        dense = dense_layer(inp, 256, 128, 'test')
        self.assertIsNotNone(dense)

    def test_rnn_cell(self):
        Win = tf.placeholder(tf.float32, [256, 128])
        Wout = tf.placeholder(tf.float32, [128, 256])
        Wfwd = tf.placeholder(tf.float32, [128, 256])
        b = tf.placeholder(tf.float32, [1, 256])
        hprev = tf.placeholder(tf.float32, [1, 256])
        inp = tf.placeholder(tf.float32, [1, 256])
        h, out = rnn_cell(Win, Wout, Wfwd, b, hprev, inp)
        self.assertIsNotNone(h)
        self.assertIsNotNone(out)
        
if __name__ == "__main__":
    unittest.main()
