from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.datasets import mnist
from keras.utils import np_utils

model = Sequential()
model.add(Convolution2D(4, 5, 5, border_mode='valid', input_shape=(1, 28, 28)))
model.add(Activation('tanh'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(8, 3, 3, border_mode='valid'))
model.add(Activation('tanh'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(16, 3, 3, border_mode='valid'))
model.add(Activation('tanh'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(128, init='uniform'))
model.add(Activation('tanh'))

model.add(Dense(10, init='uniform'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.04, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# X_train = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2])
# X_test = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2])
X_train = x_train.reshape(60000,1,28,28)
X_test = x_test.reshape(10000,1,28,28)
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

model.fit(X_train, Y_train, batch_size=100, nb_epoch=10, shuffle=True, verbose=1, validation_split=0.1)

print '\ntest set'

loss, matrics = model.evaluate(X_test, Y_test, batch_size=200, verbose=1)
print "- loss:", loss, "- acc:", matrics,
