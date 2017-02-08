from cat_data_generator import generator as GE
import numpy
from matplotlib import pyplot

data, label = GE("../../trainning_set/DEST_CAT_OLD").get_generate_data()


pyplot.hist(label.tolist(),100)
pyplot.xlabel('score')
pyplot.xlim(-8 ,8)
pyplot.ylabel('Frequency')
pyplot.title('Score distribution')
pyplot.show()
