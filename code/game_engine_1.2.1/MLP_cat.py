from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from cat_data_generator import generator as GE
from keras.utils import np_utils
import numpy

model = Sequential()
model.add(Dense(100, input_dim=11*8*8, init='uniform'))
model.add(Activation('sigmoid'))
model.add(Dropout(0.5))

# model.add(Dense(400, init='uniform'))
# model.add(Activation('sigmoid'))
# # model.add(Dropout(0.5))
#
# model.add(Dense(300, init='uniform'))
# model.add(Activation('sigmoid'))
# # model.add(Dropout(0.5))
#
# model.add(Dense(200, init='uniform'))
# model.add(Activation('sigmoid'))
# model.add(Dropout(0.5))

# model.add(Dense(100, init='uniform'))
# model.add(Activation('sigmoid'))
# model.add(Dropout(0.5))

# model.add(Dense(50, init='uniform'))
# model.add(Activation('sigmoid'))
# model.add(Dropout(0.5))

# model.add(Dense(16, init='uniform'))
# model.add(Activation('tanh'))
# model.add(Dropout(0.5))

model.add(Dense(41, init='uniform'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


data, label = GE("../../trainning_set/DEST_CAT_OLD").get_generate_data()

x_train = data[0:12000,:,:,:]
x_test = data[12000:,:,:,:]
y_train = label[0:12000]
y_test = label[12000:]


X_train = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
X_test = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
Y_train = np_utils.to_categorical(label[0:12000], 41)
Y_test = np_utils.to_categorical(label[12000:], 41)
# Y_train = y_train
# Y_test = y_test

model.fit(X_train, Y_train, batch_size=200, nb_epoch=20, shuffle=True, verbose=1, validation_split=0.1)

print '\ntest set'

loss, matrics = model.evaluate(X_test, Y_test, batch_size=200, verbose=1)
print "- loss:", loss, "- accuracy:", matrics,

model.save('MLP_cat_model.h5')
