from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from score_data_generator import generator as GE
import numpy

model = Sequential()
model.add(Dense(500, input_dim=320, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(400, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(300, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(200, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(100, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(50, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(16, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

model.add(Dense(1, init='uniform'))
# model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['mean_absolute_percentage_error'])


data, label = GE("../../trainning_set/DEST_SCORE").get_generate_data()

x_train = data[0:12000,:,:,:]
x_test = data[12000:,:,:,:]
y_train = label[0:12000]
y_test = label[12000:]


X_train = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
X_test = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
Y_train = y_train
Y_test = y_test

model.fit(X_train, Y_train, batch_size=200, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.1)

print '\ntest set'

loss, matrics = model.evaluate(X_test, Y_test, batch_size=200, verbose=1)
print "- loss:", loss, "- mean_absolute_percentage_error:", matrics,

model.save('MLP_score_model.h5')
