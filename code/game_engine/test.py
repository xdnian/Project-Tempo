# from data_generator import generator as ge
from score_data_generator import generator as ge



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

new_ge = ge("../../trainning_set/DEST_SCORE_OLD")
data, label = new_ge.get_generate_data()
print data[0],data[1],data[2]
