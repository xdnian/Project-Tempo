from keras.models import Sequential, load_model
from keras.utils import np_utils
import matplotlib.pyplot as plt
import numpy as np
import os
import time

model = load_model('./model/CNN_cat_10_model_L_201704062154.h5')

f1 = file("cat_training_set_10_L.npy", "rb")
data_train = np.load(f1)
label_train = np.load(f1)

X_test = np.asarray(data_train[600000:660000,:,:,:])
Y_test = np_utils.to_categorical(label_train[600000:660000], 17)

print "\nTEST"
loss, matrics = model.evaluate(X_test, Y_test, batch_size=500, verbose=1)
print "- loss:", loss, "- accuracy:", matrics