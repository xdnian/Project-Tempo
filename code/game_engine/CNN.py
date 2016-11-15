from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from data_generator import generator as GE
import numpy as np

model = Sequential()
model.add(Convolution2D(4, 2, 2, activation='tanh', border_mode='valid', input_shape=(5, 8, 8)))
# model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(8, 2, 2, activation='tanh', border_mode='valid'))
# model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

model.add(Convolution2D(16, 4, 4, activation='tanh', border_mode='valid'))
# model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

model.add(Flatten())
model.add(Dense(128, init='uniform'))
model.add(Activation('tanh'))

model.add(Dense(64, init='uniform'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.04, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

data, label = GE("data.txt").get_generate_data()


X_train = np.asarray(data[0:12000,:,:,:])
X_test = np.asarray(data[12000:-1,:,:,:])
Y_train = np_utils.to_categorical(label[0:12000], 64)
Y_test = np_utils.to_categorical(label[12000:-1], 64)

model.fit(X_train, Y_train, batch_size=50, nb_epoch=50, shuffle=True, verbose=1, validation_split=0.1)

print '\ntest set'

loss, matrics = model.evaluate(X_test, Y_test, batch_size=25, verbose=1)
print "- loss:", loss, "- acc:", matrics,
