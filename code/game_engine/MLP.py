from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from data_generator import generator as GE
import numpy

model = Sequential()
model.add(Dense(200, input_dim=320, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(150, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(64, init='uniform'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


data, label = GE("data.txt").get_generate_data()

x_train = data[0:12000,:,:,:]
x_test = data[12000:-1,:,:,:]
y_train = label[0:12000]
y_test = label[12000:-1]


X_train = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
X_test = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
Y_train = (numpy.arange(64) == y_train[:, None]).astype(int)
Y_test = (numpy.arange(64) == y_test[:,None]).astype(int)

model.fit(X_train, Y_train, batch_size=200, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.1)

print '\ntest set'

loss, matrics = model.evaluate(X_test, Y_test, batch_size=200, verbose=1)
print "- loss:", loss, "- acc:", matrics,
