import os
import time
import glob
import math

def sim_convert(line):
    value = float(line[6:])
    # if value < 1 and value > -1:
    #     if value > 0:
    #         value = 1.5
    #     elif value < 0:
    #         value = -1.5
    value = 16 / (1 + math.exp(-value/4.5)) - 8
    value = int(round(value))
    if value > 8:
        value = 8
    elif value < -8:
        value = -8
    return line[0:6]+str(value)


START_TIME = time.time()

print('File convertion begin...')

DATA_DIR = os.getcwd() + '/DEST_SCORE/'
# converted data file in \DEST_CAT_OLD
DEST_DIR = os.getcwd() + '/DEST_CAT/'

# print DATA_DIR, DEST_DIR, os.listdir(DATA_DIR)

FILE_CNT = 0

for filepath in glob.glob(DATA_DIR+'*.txt'):

    # get file name without the path
    _, filename = os.path.split(filepath)
    # creat desination data fiel with DEST_DIR path
    destfile = DEST_DIR + filename

    try:
        # open the file in DATA_DIR for reading
        inputfile = open(filepath)
        # open a same-name file in DEST_DIR for writing
        outputfile = open(destfile, 'w')

        for line in inputfile:
            outputfile.write(sim_convert(line)+'\n')

        inputfile.close()
        outputfile.close()

    except Exception as msg:
        print("Error at \"" + filename +"\": ")
        print(msg)
        print('Continue...')
        # inputfile.close()
        # outputfile.close()
        # os.unlink(outputfile.name)

    else:
        FILE_CNT += 1


print('File convertion finished: ')
RUNNING_TIME = round(time.time() - START_TIME, 3)
print("\tTotal running time: " + str(RUNNING_TIME) + " seconds.")
print("\t" + str(FILE_CNT) + " file(s) converted.")
