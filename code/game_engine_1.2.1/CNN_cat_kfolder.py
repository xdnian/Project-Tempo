from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from cat_data_generator import generator as GE
import numpy as np
import os
import time
# from sklearn.cross_validation import StratifiedKFold

def create_model():
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, activation='sigmoid', border_mode='valid', input_shape=(11, 8, 8)))
    # model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(64, 3, 3, activation='sigmoid', border_mode='valid'))
    # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # model.add(Convolution2D(4, 2, 2, activation='tanh', border_mode='valid'))
    # # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    model.add(Dropout(0.2))

    model.add(Flatten())
    # model.add(Dense(512, init='uniform'))
    # model.add(Activation('tanh'))

    model.add(Dense(256, init='uniform'))
    model.add(Activation('tanh'))

    model.add(Dropout(0.2))

    model.add(Dense(128, init='uniform'))
    model.add(Activation('tanh'))

    model.add(Dropout(0.2))

    model.add(Dense(17, init='uniform'))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.04, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    return model

def train_and_evaluate_model(model, X_train, Y_train, X_test, Y_test):
    hist = model.fit(X_train, Y_train, batch_size=1000, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.0)
    loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
    print "- loss:", loss, "- accuracy:", matrics
    return hist, loss, matrics


if __name__=='__main__':

    Start = time.time()

    f = file("cat_training_set_L.npy", "rb")
    data = np.load(f)
    label = np.load(f)

    X_train = np.asarray(data[0:600000,:,:,:])
    X_test = np.asarray(data[600000:660000,:,:,:])
    Y_train = np_utils.to_categorical(label[0:600000], 17)
    Y_test = np_utils.to_categorical(label[600000:660000], 17)

    # EX
    # X_train = np.asarray(data[0:1300000,:,:,:])
    # X_test = np.asarray(data[1300000:1375000,:,:,:])
    # Y_train = np_utils.to_categorical(label[0:1300000], 17)
    # Y_test = np_utils.to_categorical(label[1300000:1375000], 17)

    # # with k_fold
    # k_fold=10
    # best_model = None
    # best_acc = 0
    # skf = StratifiedKFold(Y_train, n_folds=n_folds, shuffle=True)
    # with open(time.strftime("./result/CNN_cat_train_%Y%m%d%H%M.txt"), "w") as f:
    #     for i, (train, test) in enumerate(skf):
    #         print "Running Fold", i+1, "/", n_folds
    #         model = None # Clearing the NN.
    #         model = create_model()
    #         hist, loss, matrics = train_and_evaluate_model(model, X_train[train], Y_train[train], X_test[test], Y_test[test])
    #         if best_acc < matrics:
    #             best_model = model
    #         f.write(hist.history)
    #
    # print '\ntest set'
    #
    # loss, matrics = best_model.evaluate(X_test, Y_test, batch_size=2000, verbose=1)
    # print "- loss:", loss, "- accuracy:", matrics,

    # without k_fold
    model = create_model()
    # best_model = load_model('./model/CNN_cat_model_L_500.h5')

    hist = model.fit(X_train, Y_train, batch_size=1000, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.1)
    print "\nTEST"
    loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
    print "- loss:", loss, "- accuracy:", matrics

    End = time.time()
    print round(End-Start,3)
