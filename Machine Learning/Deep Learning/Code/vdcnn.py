import tensorflow as tf
from keras.models import Model
from keras.layers.convolutional import Conv1D
from keras.layers.embeddings import Embedding
from keras.layers import Input, Dense, Dropout, Lambda
from keras.layers.pooling import MaxPooling1D
from keras.optimizers import SGD
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers import Activation
import numpy as np

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:\'\"/\\|_@#$%^&*~`+ =<>()[]{}"  # len: 69
FEATURE_LEN = 1024

def get_char_dict():
    cdict = {}
    for i, c in enumerate(ALPHABET):
        cdict[c] = i + 2

    return cdict


def get_comment_ids(text, max_length=FEATURE_LEN):
    array = np.ones(max_length)
    count = 0
    cdict = get_char_dict()

    for ch in text:
        if ch in cdict:
            array[count] = cdict[ch]
            count += 1

        if count >= FEATURE_LEN - 1:
            return array

    return array


def to_categorical(y, nb_classes=None):
    y = np.asarray(y, dtype='int32')

    if not nb_classes:
        nb_classes = np.max(y) + 1

    Y = np.zeros((len(y), nb_classes))
    for i in range(len(y)):
        Y[i, y[i]] = 1.

    return Y


def conv_shape(conv):
    return conv.get_shape().as_list()[1:]

def ConvBlockLayer(input_shape, num_filters):

    model = Sequential()
    """
    two layer ConvNet. Apply batch_norm and relu after each layer
    """

    # first conv layer
    model.add(Conv1D(filters=num_filters, kernel_size=3, strides=1, padding="same", input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    # second conv layer
    model.add(Conv1D(filters=num_filters, kernel_size=3, strides=1, padding="same"))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    return model

#https://www.tensorflow.org/api_docs/python/tf/nn/top_k
def top_kmax(x):
    x=tf.transpose(x, [0, 2, 1])
    k_max = tf.nn.top_k(x, k=top_k)
    return tf.reshape(k_max[0], (-1, num_filters[-1]*top_k))


def build_model(num_filters, num_classes, sequence_max_length=1024, dropout=0.,
                num_quantized_chars=69, embedding_size=16, learning_rate=0.01, top_k=3,
                model_path=None):

    inputs = Input(shape=(sequence_max_length, ), dtype='int32', name='inputs')
    embedded_sent = Embedding(num_quantized_chars, embedding_size, input_length=sequence_max_length)(inputs)
    embedded_sent = BatchNormalization()(embedded_sent)

    # First conv layer
    conv = Conv1D(filters=64, kernel_size=3, strides=2, padding="same")(embedded_sent)

    #ConvBlocks
    for i in range(len(num_filters)):
        conv = ConvBlockLayer(conv_shape(conv), num_filters[i])(conv)
        conv = MaxPooling1D(pool_size=3, strides=2, padding="same")(conv)

    def _top_k(x):
        x = tf.transpose(x, [0, 2, 1])
        k_max = tf.nn.top_k(x, k=top_k)
        return tf.reshape(k_max[0], (-1, num_filters[-1] * top_k))

    k_max = Lambda(_top_k, output_shape=(num_filters[-1] * top_k,))(conv)

    #fully connected layers
    # in original paper they didn't used dropouts
    fc1=Dropout(0.)(Dense(512, activation='relu', kernel_initializer='he_normal')(k_max))
    fc2=Dropout(0.)(Dense(512, activation='relu', kernel_initializer='he_normal')(fc1))
    fc3=Dense(num_classes, activation='sigmoid')(fc2)

    # define optimizer
    sgd = SGD(lr=learning_rate, decay=1e-6, momentum=0.9, nesterov=False)
    model = Model(inputs=inputs, outputs=fc3)
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

    if model_path is not None:
        model.load_weights(model_path)

    return model
