# from data_generator import generator as ge
# from score_data_generator import generator as ge
from cat_data_generator import generator as GE
import numpy as np
from keras.models import load_model
from keras.models import Sequential
from keras.utils import np_utils



# new_ge = ge("data.txt")
# data, label = new_ge.get_generate_data()
# print label
# print data[1], label[1]

# length = 0
# print sum(1 for line in open('test.txt'))
# with open("test.txt", 'r') as f:
#     for line in f:
#         for i in xrange(3):
#             print int(line[i*2])
#         print float(line[6:])

# new_ge = ge("../../trainning_set/DEST_SCORE_OLD")
# data, label = new_ge.get_generate_data()
# print data[0],data[1],data[2]

data, label = GE("../../trainning_set/DEST_CAT_OLD").get_generate_data()

model = load_model("CNN_cat_model.h5")

X_train = np.asarray(data[0:12000,:,:,:])
X_test = np.asarray(data[12000:,:,:,:])
Y_train = np_utils.to_categorical(label[0:12000], 17)
Y_test = np_utils.to_categorical(label[12000:], 17)

predict_label = model.predict(X_train, batch_size=1, verbose=1)
accsum = 0
for i in xrange(12000):
    if np.argmax(predict_label[i]) == np.argmax(Y_train[i]):
        accsum += 1
print "the acc for trainging set is:", accsum/12000.0

predict_label = model.predict(X_test, batch_size=1, verbose=1)
accsum = 0
for i in xrange(1911):
    if np.argmax(predict_label[i]) == np.argmax(Y_train[i]):
        accsum += 1
print "the acc for testing set is:", accsum/1911.0
