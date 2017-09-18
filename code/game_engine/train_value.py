'''
value network train
'''
import os
import time
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
import matplotlib.pyplot as plt
import numpy as np

def create_model(k):
    model = Sequential()

    model.add(Conv2D(k, kernel_size=(5, 5), activation='relu', padding='same', input_shape=(10, 8, 8)))

    for i in xrange(4):
        model.add(Conv2D(k, kernel_size=(3, 3), activation='relu', padding='same'))

    model.add(Conv2D(1, kernel_size=(1, 1), activation='linear', padding='same'))

    model.add(Flatten())

    model.add(Dense(128, activation='linear'))

    model.add(Dense(1, activation='tanh'))

    sgd = keras.optimizers.SGD(lr=0.04, momentum=0.0, decay=0.0, nesterov=False)
    model.compile(loss=keras.losses.mean_squared_error,
                  optimizer=sgd,
                  metrics=['mae'])

    return model

# def train_and_evaluate_model(model, X_train, Y_train, X_test, Y_test):
#     hist = model.fit(X_train, X_test, batch_size=1000, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.0)
#     loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
#     print "- loss:", loss, "- accuracy:", matrics
#     return hist, loss, matrics


if __name__=='__main__':

    Start = time.time()

    f = file("./dataset/value_training_data.npy", "rb")
    data_train = np.load(f)
    label_train = np.load(f)

    X_train = np.asarray(data_train[0:6000000, :, :, :])
    X_test = np.asarray(data_train[6000000:6500000, :, :, :])
    Y_train = np.asarray(label_train[0:6000000])
    Y_test = np.asarray(label_train[6000000:6500000])


    model = create_model(128)
    # model = load_model('./model/CNN_cat_model_L_500.h5')

    epochs = 2
    interval = 10
    batch_size = 10000
    train_scores = []
    val_scores = []

    for i in xrange(interval):
        print i, '/', interval
        hist = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, shuffle=True, verbose=1, validation_split=0.1)
        if i == 0:
            train_scores.append(hist.history['loss'][0])
            val_scores.append(hist.history['val_loss'][0])
        train_scores.append(hist.history['loss'][epochs-1])
        val_scores.append(hist.history['val_loss'][epochs-1])

    print "\nTEST"
    loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
    print "- loss:", loss, "- mae:", matrics

    model.save(time.strftime('./model/value_model_L_epochs_%Y%m%d%H%M.h5'))

    plt.plot(range(interval+1), train_scores,
             color='blue', marker='o',
             markersize=5, label='training MSE')

    plt.plot(range(interval+1), val_scores,
             color='green', linestyle='--',
             marker='s', markersize=5,
             label='validation MSE')

    plt.grid()
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend(loc='lower right')
    plt.ylim([0.0, 1.0])
    plt.tight_layout()
    plt.savefig(time.strftime('./figures/value_learning_curve_%Y%m%d%H%M.png'), dpi=300)
    plt.show()


    End = time.time()
    print round(End-Start, 3)
