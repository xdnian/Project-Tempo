from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
import matplotlib.pyplot as plt
# from cat_data_generator import generator as GE
import numpy as np
import os
import time
# from sklearn.cross_validation import StratifiedKFold

def create_model():
    model = Sequential()
    model.add(Convolution2D(64, 4, 4, activation='relu', border_mode='same', input_shape=(10, 8, 8)))
    # model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(128, 3, 3, activation='relu', border_mode='same'))
    # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # model.add(Convolution2D(128, 3, 3, activation='relu', border_mode='same'))

    # model.add(Convolution2D(4, 2, 2, activation='tanh', border_mode='valid'))
    # # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # model.add(Dropout(0.3))

    model.add(Flatten())
    # model.add(Dense(512, init='uniform'))
    # model.add(Activation('tanh'))

    model.add(Dense(256, init='uniform'))
    model.add(Activation('tanh'))

    model.add(Dense(128, init='uniform'))
    model.add(Activation('tanh'))

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

    f = file("cat_training_set_L_NEW.npy", "rb")
    data = np.load(f)
    label = np.load(f)
    print data.shape, label.shape
    X_train = np.asarray(data[0:600000,:,:,:])
    X_test = np.asarray(data[600000:660000,:,:,:])
    Y_train = np_utils.to_categorical(label[0:600000], 17)
    Y_test = np_utils.to_categorical(label[600000:660000], 17)

    # # EX
    # f = file("cat_training_set_EX.npy", "rb")
    # data = np.load(f)
    # label = np.load(f)
    # X_train = np.asarray(data[0:1200000,:,:,:])
    # X_test = np.asarray(data[1200000:1375000,:,:,:])
    # Y_train = np_utils.to_categorical(label[0:1200000], 17)
    # Y_test = np_utils.to_categorical(label[1200000:1375000], 17)


    model = create_model()
    # model = load_model('./model/CNN_cat_model.h5')

    nepoch = 10
    interval = 15
    train_scores = []
    val_scores = []

    for i in xrange(interval):
        print i, '/', interval
        hist = model.fit(X_train, Y_train, batch_size=2000, nb_epoch=nepoch, shuffle=True, verbose=1, validation_split=0.1)
        if i == 0:
            train_scores.append(hist.history['acc'][0])
            val_scores.append(hist.history['val_acc'][0])
        train_scores.append(hist.history['acc'][nepoch-1])
        val_scores.append(hist.history['val_acc'][nepoch-1])

    print "\nTEST"
    loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
    print "- loss:", loss, "- accuracy:", matrics

    model.save(time.strftime('./model/CNN_cat_model_L_%Y%m%d%H%M.h5'))

    plt.plot(range(interval+1), train_scores,
             color='blue', marker='o',
             markersize=5, label='training accuracy')

    plt.plot(range(interval+1), val_scores,
             color='green', linestyle='--',
             marker='s', markersize=5,
             label='validation accuracy')

    plt.grid()
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.ylim([0.0, 1.0])
    plt.tight_layout()
    # plt.savefig(time.strftime('./figures/CNN_cat_tuning_epoch_learning_curve_%Y%m%d%H%M.png'), dpi=300)
    plt.show()


    End = time.time()
    print round(End-Start,3)
