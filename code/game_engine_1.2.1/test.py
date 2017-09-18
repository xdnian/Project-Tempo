import numpy as np
f2 = file("p_test_set_10.npy", "rb")
data_test = np.load(f2)
label_test = np.load(f2)
print data_test.shape
print label_test.shape
