from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
import argparse

def reading_terminal_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epoch", help="number of epochs")
    parser.add_argument("--bsize", help="batch size")

    args = parser.parse_args()

    epoch = int(args.epoch) if args.epoch else 4
    bsize = int(args.bsize) if args.bsize else 200

    return epoch , bsize

def loading_data():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    num_pixels = X_train.shape[1] * X_train.shape[2]
    X_train = X_train.reshape((X_train.shape[0], num_pixels)).astype('float32')
    X_test = X_test.reshape((X_test.shape[0], num_pixels)).astype('float32')

    X_train = X_train[1:5000] / 255
    X_test = X_test / 255

    y_train = np_utils.to_categorical(y_train[1:5000])
    y_test = np_utils.to_categorical(y_test)
    num_classes = y_test.shape[1]

    return (X_train,y_train), (X_test,y_test)


# define baseline model
def architecture():

    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(10))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

    return model
