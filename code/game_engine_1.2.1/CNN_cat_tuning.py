import numpy as np
import os
import time

from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import StratifiedKFold

# bug fix
from keras.wrappers.scikit_learn import BaseWrapper
import copy
def custom_get_params(self, **params):
    res = copy.deepcopy(self.sk_params)
    res.update({'build_fn': self.build_fn})
    return res
BaseWrapper.get_params = custom_get_params
# bug fix /

np.random.seed(7)

def create_model(dropout_rate=0.3, conv_act='sigmoid'):
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, activation=conv_act, border_mode='valid', input_shape=(11, 8, 8)))
    # model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(64, 3, 3, activation=conv_act, border_mode='valid'))
    # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # model.add(Convolution2D(4, 2, 2, activation='tanh', border_mode='valid'))
    # # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    model.add(Dropout(dropout_rate))

    model.add(Flatten())
    # model.add(Dense(512, init='uniform'))
    # model.add(Activation('tanh'))

    model.add(Dense(256, init='uniform'))
    model.add(Activation('tanh'))

    model.add(Dense(128, init='uniform'))
    model.add(Activation('tanh'))

    # model.add(Dropout(dropout_rate))

    model.add(Dense(17, init='uniform'))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.04, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    return model

# def train_and_evaluate_model(model, X_train, Y_train, X_test, Y_test):
#     hist = model.fit(X_train, X_test, batch_size=1000, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.0)
#     loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
#     print "- loss:", loss, "- accuracy:", matrics
#     return hist, loss, matrics


if __name__=='__main__':

    Start = time.time()

    f = file("cat_training_set_L.npy", "rb")
    data = np.load(f)
    label = np.load(f)

    # tuning L
    X_train = np.asarray(data[0:660000,:,:,:])
    Y_train = np_utils.to_categorical(label[0:660000], 17)

    # L
    # X_train = np.asarray(data[0:600000,:,:,:])
    # X_test = np.asarray(data[600000:660000,:,:,:])
    # Y_train = np_utils.to_categorical(label[0:600000], 17)
    # Y_test = np_utils.to_categorical(label[600000:660000], 17)

    # EX
    # X_train = np.asarray(data[0:1300000,:,:,:])
    # X_test = np.asarray(data[1300000:1375000,:,:,:])
    # Y_train = np_utils.to_categorical(label[0:1300000], 17)
    # Y_test = np_utils.to_categorical(label[1300000:1375000], 17)

    model = KerasClassifier(build_fn=create_model, nb_epoch=300, batch_size=2000, verbose=1)

    # dropout_rates = np.arange(0, 1, 0.1)
    activations = ['tanh', 'relu', 'sigmoid', 'softplus', 'elu']
    # activations = ['tanh', 'relu', 'sigmoid']
    # activations = ['tanh']
    param_grid = dict(conv_act=activations)
    gs = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=1)
    grid_result = gs.fit(X_train, Y_train)

    print 'Best:', grid_result.best_score_, 'using', grid_result.best_params_
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print mean, '(', stdev, ') with:', param

    End = time.time()
    print '\nTotal time:', round(End-Start,3)
