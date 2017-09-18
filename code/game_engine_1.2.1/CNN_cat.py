from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Flatten
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
    model.add(Convolution2D(32, 3, 3, activation='tanh', border_mode='valid', input_shape=(11, 8, 8)))
    # model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(64, 3, 3, activation='tanh', border_mode='valid'))
    # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # model.add(Convolution2D(4, 2, 2, activation='tanh', border_mode='valid'))
    # # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

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

def train_and_evaluate_model(model, X_train, Y_train, X_test, Y_test):
    hist = model.fit(X_train, Y_train, batch_size=1000, nb_epoch=500, shuffle=True, verbose=1, validation_split=0.1)
    loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
    print "- loss:", loss, "- accuracy:", matrics
    return hist, loss, matrics


if __name__=='__main__':

    Start = time.time()

    f = file("cat_training_set_L.npy", "rb")
    data = np.load(f)
    label = np.load(f)

    data_train = np.asarray(data[0:600000,:,:,:])
    data_test = np.asarray(data[600000:660000,:,:,:])
    label_train = np_utils.to_categorical(label[0:600000], 17)
    label_test = np_utils.to_categorical(label[600000:660000], 17)

    # EX
    # data_train = np.asarray(data[0:1300000,:,:,:])
    # data_test = np.asarray(data[1300000:1375000,:,:,:])
    # label_train = np_utils.to_categorical(label[0:1300000], 17)
    # label_test = np_utils.to_categorical(label[1300000:1375000], 17)

    # model = create_model()
    model = load_model('./model/CNN_cat_model_L_500.h5')
    for i in xrange(5):
        hist, loss, matrics = train_and_evaluate_model(model, data_train, label_train, data_test, label_test)
        with open(time.strftime("./result/CNN_cat_train_L_"+str(600+i*100)+"_%Y%m%d%H%M.txt"), "w") as f:
            f.write(str(hist.history))

        model.save('./model/CNN_cat_model_L_'+str(600+i*100)+'.h5')

    End = time.time()
    print round(End-Start,3)
