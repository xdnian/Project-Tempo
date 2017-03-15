from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from score_data_generator_distinct import generator as GE
import numpy as np
import os
import time

model = Sequential()
model.add(Convolution2D(16, 4, 4, activation='sigmoid', border_mode='valid', input_shape=(9, 8, 8)))
# model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(16, 2, 2, activation='sigmoid', border_mode='valid'))
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

# # Use small data set
# data, label = GE("../../trainning_set/DEST_SCORE_OLD").get_generate_data()
# X_train = np.asarray(data[0:11000,:,:,:])
# X_test = np.asarray(data[11000:12200,:,:,:])
# Y_train = np.asarray(label[0:11000])
# Y_test = np.asarray(label[11000:12200])

# USE large data set
data, label = GE("../../trainning_set/DEST_SCORE").get_generate_data()
X_train = np.asarray(data[0:180000,:,:,:])
X_test = np.asarray(data[180000:190000,:,:,:])
Y_train = np.asarray(label[0:180000])
Y_test = np.asarray(label[180000:190000])


hist = model.fit(X_train, Y_train, batch_size=200, nb_epoch=100, shuffle=True, verbose=1, validation_split=0.1)
with open(time.strftime("./result/CNN_score_%Y%m%d%H%M.txt"), "w") as f:
    f.write(hist.history)

print '\ntest set'

loss, matrics = model.evaluate(X_test, Y_test, batch_size=25, verbose=1)
print "- loss:", loss, "- mean_squared_error:", matrics,

model.save('CNN_score_model.h5')
