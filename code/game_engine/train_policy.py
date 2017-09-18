'''
policy network train
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

    model.add(Activation('softmax'))

    sgd = keras.optimizers.SGD(lr=0.04, momentum=0.0, decay=0.0, nesterov=False)
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=sgd,
                  metrics=['accuracy'])

    return model

# def train_and_evaluate_model(model, X_train, Y_train, X_test, Y_test):
#     hist = model.fit(X_train, X_test, batch_size=1000, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.0)
#     loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
#     print "- loss:", loss, "- accuracy:", matrics
#     return hist, loss, matrics


if __name__=='__main__':

    Start = time.time()

    f1 = file("./dataset/policy_training_data.npy", "rb")
    data_train = np.load(f1)
    label_train = np.load(f1)

    X_train = np.asarray(data_train[0:600000, :, :, :])
    X_test = np.asarray(data_train[600000:660000, :, :, :])
    Y_train = np_utils.to_categorical(label_train[0:600000], 64)
    # Y_train = np.reshape(Y_train, (600000, 1, 8, 8))
    Y_test = np_utils.to_categorical(label_train[600000:660000], 64)
    # Y_test = np.reshape(Y_test, (60000, 1, 8, 8))

    # # EX
    # f = file("cat_training_set_EX.npy", "rb")
    # data = np.load(f)
    # label = np.load(f)
    # X_train = np.asarray(data[0:1200000,:,:,:])
    # X_test = np.asarray(data[1200000:1375000,:,:,:])
    # Y_train = np_utils.to_categorical(label[0:1200000], 17)
    # Y_test = np_utils.to_categorical(label[1200000:1375000], 17)


    model = create_model(128)
    # model = load_model('./model/CNN_cat_model_L_500.h5')

    epochs = 2
    interval = 10
    batch_size = 500
    train_scores = []
    val_scores = []

    for i in xrange(interval):
        print i, '/', interval
        hist = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, shuffle=True, verbose=1, validation_split=0.1)
        if i == 0:
            train_scores.append(hist.history['acc'][0])
            val_scores.append(hist.history['val_acc'][0])
        train_scores.append(hist.history['acc'][epochs-1])
        val_scores.append(hist.history['val_acc'][epochs-1])

    print "\nTEST"
    loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
    print "- loss:", loss, "- accuracy:", matrics

    model.save(time.strftime('./model/policy_model_L_epochs_%Y%m%d%H%M.h5'))

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
    plt.savefig(time.strftime('./figures/policy_learning_curve_%Y%m%d%H%M.png'), dpi=300)
    plt.show()


    End = time.time()
    print round(End-Start, 3)
