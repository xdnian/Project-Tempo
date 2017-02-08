from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from cat_data_generator import generator as GE
import numpy as np

model = Sequential()
model.add(Convolution2D(32, 3, 3, activation='sigmoid', border_mode='valid', input_shape=(11, 8, 8)))
# model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 3, 3, activation='sigmoid', border_mode='valid'))
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

data, label = GE("../../trainning_set/DEST_CAT").get_generate_data()


X_train = np.asarray(data[0:250000,:,:,:])
X_test = np.asarray(data[250000:,:,:,:])
Y_train = np_utils.to_categorical(label[0:250000], 17)
Y_test = np_utils.to_categorical(label[250000:], 17)

# for i in range(100):
#     print label[i]
#     print Y_train[i]
#     raw_input()

model.fit(X_train, Y_train, batch_size=2000, nb_epoch=500, shuffle=True, verbose=1, validation_split=0.1)

print '\ntest set'

loss, matrics = model.evaluate(X_test, Y_test, batch_size=200, verbose=1)
print "- loss:", loss, "- accuracy:", matrics,

model.save('CNN_cat_large_model.h5')
