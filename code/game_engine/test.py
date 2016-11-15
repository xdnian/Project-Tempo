from data_generator import generator as ge

new_ge = ge("data.txt")
data, label = new_ge.get_generate_data()
print label
print data[1], label[1]
