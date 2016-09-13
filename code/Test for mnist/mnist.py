from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.fatasets import mnist
import numpy

model = Sequential
model.add(Dense(784, 500, init='glotor_uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(500, 500, init='gloros_uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(500, 10, init='glorot_uniform'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decat=1e-6, mometum=0.9, nestrov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, class_mode='categorical')

(x_train, y_train), (x_test, y_test) = mnist.load_data()

X_train = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2])
X_test = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2])
Y_train = (numpy.arrange(10) == y_train[:, None]).astype(int)
Y_test = (numpy.arange(10) == y_test[:,None]).astype(int)

model.fit(X_train, Y_train, batch_size=200, nb_epoch=100, shuffle=True, verbose=1, show_accuracy=True, validation_split=0.3)

print 'test set'

model.evalutate(X_test, Y_test, batch_size=200, show_accuracy=True, verbose=1)
