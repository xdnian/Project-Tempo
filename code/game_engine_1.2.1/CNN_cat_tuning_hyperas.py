from __future__ import print_function
from hyperopt import Trials, STATUS_OK, rand
from hyperas import optim
from hyperas.distributions import choice, uniform, conditional
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
import numpy
import os
import time
# from sklearn.cross_validation import StratifiedKFold

def data():
    f = file("cat_training_set_L.npy", "rb")
    data = numpy.load(f)
    label = numpy.load(f)
    f.close()

    X_train = numpy.asarray(data[0:600000,:,:,:])
    X_test = numpy.asarray(data[600000:660000,:,:,:])
    Y_train = np_utils.to_categorical(label[0:600000], 17)
    Y_test = np_utils.to_categorical(label[600000:660000], 17)

    # EX
    # X_train = numpy.asarray(data[0:1300000,:,:,:])
    # X_test = numpy.asarray(data[1300000:1375000,:,:,:])
    # Y_train = np_utils.to_categorical(label[0:1300000], 17)
    # Y_test = np_utils.to_categorical(label[1300000:1375000], 17)

    return X_train, Y_train, X_test, Y_test

def model(X_train, Y_train, X_test, Y_test):
    model = Sequential()
    k_size_1 = {{choice[3, 4]}}
    model.add(Convolution2D({{choice[16, 32]}}, k_size_1, k_size_1, activation='sigmoid', border_mode='valid', input_shape=(11, 8, 8)))
    # model.add(MaxPooling2D(pool_size=(2, 2)))

    k_size_2 = {{choice[2, 3]}}
    model.add(Convolution2D({{choice[16, 32, 64]}}, k_size_2, k_size_2, activation='sigmoid', border_mode='valid'))
    # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # model.add(Convolution2D(4, 2, 2, activation='tanh', border_mode='valid'))
    # # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    model.add(Dropout({{uniform(0, 1)}}))

    model.add(Flatten())
    # model.add(Dense(512, init='uniform'))
    # model.add(Activation('tanh'))

    model.add(Dense({{choice[64, 128, 256]}}, init='uniform'))
    model.add(Activation('tanh'))

    model.add(Dropout({{uniform(0, 1)}}))

    model.add(Dense({{choice[32, 64, 128]}}, init='uniform'))
    model.add(Activation('tanh'))

    model.add(Dropout({{uniform(0, 1)}}))

    model.add(Dense(17, init='uniform'))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.04, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer={{choice['sgd', 'Adam', 'Adamax', 'Adadelta']}}, metrics=['accuracy'])

    model.fit(X_train, Y_train, batch_size=2000, nb_epoch=50, shuffle=True, verbose=1, validation_split=0.1)
    print("TEST")
    loss, metrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
    print("- loss:", loss, "- accuracy:", metrics)
    return {'loss': -metrics, 'status': STATUS_OK, 'model': model}


if __name__=='__main__':

    Start = time.time()

    best_run, best_model = optim.minimize(model=model,
                                          data=data,
                                          algo=rand.suggest,
                                          max_evals=5,
                                          trials=Trials())
    X_train, Y_train, X_test, Y_test = data()
    print("\n=========================\nEvalutation of best performing model:")
    print(best_model.evaluate(X_test, Y_test))
    print("Best run:")
    print(best_run)
    best_model.save('./model/CNN_cat_model_L_hyperas.h5')

    End = time.time()
    print('Total time:', round(End-Start,3))
