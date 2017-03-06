from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from cat_data_generator import generator as GE
import numpy as np
from sklearn.model_selection import train_test_split

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

data, label = GE("../../trainning_set/DEST_CAT_OLD").get_generate_data()

label = np_utils.to_categorical(label, 17)

# X_train = np.asarray(data[0:12000,:,:,:])
# X_test = np.asarray(data[12000:,:,:,:])
# Y_train = np_utils.to_categorical(label[0:12000], 17)
# Y_test = np_utils.to_categorical(label[12000:], 17)


X_train, X_test, Y_train, Y_test = train_test_split(data, label, test_size=0.1, random_state=12580)

for i in xrange(100):
    print "\nTraining time:", i

    model.fit(X_train, Y_train, batch_size=200, nb_epoch=1, shuffle=True, verbose=1, validation_split=0.1)

    X_train, X_test, Y_train, Y_test = train_test_split(data, label, test_size=0.1, random_state=12580+i)

print 'test set'

loss, matrics = model.evaluate(X_test, Y_test, batch_size=200, verbose=1)
print "- loss:", loss, "- accuracy:", matrics,
print

model.save('CNN_cat_model.h5')
