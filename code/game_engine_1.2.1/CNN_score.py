from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from score_data_generator import generator as GE
import numpy as np
import os
import time

def create_model():
    model = Sequential()
    model.add(Convolution2D(32, 4, 4, activation='sigmoid', border_mode='valid', input_shape=(9, 8, 8)))
    # model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(64, 2, 2, activation='sigmoid', border_mode='valid'))
    # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # model.add(Convolution2D(4, 2, 2, activation='tanh', border_mode='valid'))
    # # model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    model.add(Flatten())
    # model.add(Dense(512, init='uniform'))
    # model.add(Activation('tanh'))
    #
    model.add(Dense(256, init='uniform'))
    model.add(Activation('sigmoid'))

    model.add(Dense(128, init='uniform'))
    model.add(Activation('sigmoid'))

    model.add(Dense(1, init='uniform'))
    model.add(Activation('sigmoid'))

    sgd = SGD(lr=0.04, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['mean_squared_error'])

    return model

def load_data():
    # # Use small data set
    # data, label = GE("../../trainning_set/DEST_SCORE_OLD").get_generate_data()
    # X_train = np.asarray(data[0:11000,:,:,:])
    # X_test = np.asarray(data[11000:12200,:,:,:])
    # Y_train = np.asarray(label[0:11000])
    # Y_test = np.asarray(label[11000:12200])

    # # USE large data set
    # f = file("score_training_set_L.npy", "rb")
    # data = np.load(f)
    # label = np.load(f)
    # X_train = np.asarray(data[0:600000,:,:,:])
    # X_test = np.asarray(data[600000:660000,:,:,:])
    # Y_train = np.asarray(label[0:600000])
    # Y_test = np.asarray(label[600000:660000])

    # USE ex large data set
    f = file("score_training_set_ex.npy", "rb")
    data = np.load(f)
    label = np.load(f)
    f.close()
    X_train = np.asarray(data[0:1300000,:,:,:])
    X_test = np.asarray(data[1300000:1375000,:,:,:])
    Y_train = np.asarray(label[0:1300000])
    Y_test = np.asarray(label[1300000:1375000])

    return X_train, X_test, Y_train, Y_test

if __name__=='__main__':
    # train
    # model = create_model()
    model = load_model('./model/CNN_score_model_500.h5')
    X_train, X_test, Y_train, Y_test = load_data()

    for i in xrange(30):
        hist = model.fit(X_train, Y_train, batch_size=1000, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.1)

        print '\nTest set' 
        loss, matrics = model.evaluate(X_test, Y_test, batch_size=100, verbose=1)
        print "- loss:", loss, "- mean_squared_error:", matrics

        with open(time.strftime("./result/CNN_score_train_EX_"+str(600+i*100)+"_%Y%m%d%H%M.txt"), "w") as f:
            f.write(str(hist.history))
            f.write("Test:{'loss':[" + str(loss) + "], 'MSE':[" + str(matrics) + ']}')

        model.save('CNN_score_model_'+str(600+i*100)+'.h5')
