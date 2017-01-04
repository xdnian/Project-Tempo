#  This is a program to convert WZebra Othello transcript(txt) to tranning set file
#  tranning set file is a simplified data file of a Othello transcript
#  Copyright: Xiaodong Nian
#  python version 2.7
# ------------------------------------------------------------------------------------------------
#  CONVERTED:{
#  a converted record are in the following format:
#  <black:1/while:0> <x> <y> (x,y start from 0 at left-bottom corner) <score>
#  1 3 5 score
#  0 2 3 score
#
#     0  1  2  3  4  5  6  7
#  7 |55|40|38|51|35|52|53|47| 7
#  6 |54|56|39|33|32|34|58|28| 6
#  5 |37|21|20| 1| 6|19|27|24| 5
#  4 |26|44|10|()|##|15|22|45| 4
#  3 |30|25| 2|##|()| 4|14|23| 3
#  2 |31|29|11| 7| 5| 3| 9|17| 2
#  1 |49|36|18|13|12| 8|43|50| 1
#  0 |59|60|16|57|42|41|46|48| 0
#     0  1  2  3  4  5  6  7
#  }
#
#  ORIGINAL:{
#  History: <move> [<eval> <analysis> <eval> <lookahead>]
#    1: d3         d3              book   2: c5         c5              book 
#    3: f6         f6              book   4: f5         f5              book 
#
#     A  B  C  D  E  F  G  H
#  1 |55|40|38|51|35|52|53|47| 1
#  2 |54|56|39|33|32|34|58|28| 2
#  3 |37|21|20| 1| 6|19|27|24| 3
#  4 |26|44|10|()|##|15|22|45| 4
#  5 |30|25| 2|##|()| 4|14|23| 5
#  6 |31|29|11| 7| 5| 3| 9|17| 6
#  7 |49|36|18|13|12| 8|43|50| 7
#  8 |59|60|16|57|42|41|46|48| 8
#     A  B  C  D  E  F  G  H
#  }

import os
import glob
import time

import linecache

START_TIME = time.time()

print('File convertion begin...')
# original file in \DATA
DATA_DIR = os.getcwd() + '\DATA\\'
# converted data file in \DEST_SCORE
DEST_DIR = os.getcwd() + '\DEST_SCORE\\'

FILE_CNT = 0

# For every txt file in the DATA_DIR
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


        # black tech, get scores from 57&58 moves as a standard to fill in the blanks in the scores
        black_standard = 0
        white_standard = 0

        target = linecache.getline(filepath, 53)
        black_s, white_s = target[8:15], target[45:52]

        if black_s.strip():
            black_standard = float(black_s)
            white_standard = 0 - black_standard
        elif white_s.strip():
            white_standard = float(white_s)
            black_standard = 0 - white_standard

        linecache.clearcache()


        # initialize line counter
        line_cnt = 0
        # for each line in the file
        for line in inputfile.readlines():
            line_cnt += 1

            # the record start at line 25
            if line_cnt > 24:
                # a space line after line 25 means the end of the record, break the loop
                if line.isspace():
                    break

                # read one turn of black
                black_cnt, black_move, black_score_s = line[1:3], line[5:7], line[8:15]

                # handle black_score
                if black_score_s.strip():
                    if black_score_s == 'Win    ':
                        black_score = 64
                    elif black_score_s == 'Loss   ':
                        black_score = -64
                    elif black_score_s == 'Draw   ':
                        black_score = 0
                    else:
                        black_score = float(black_score_s)
                else:
                    black_score = black_standard

                # if the black move is not forced to be skiped
                if black_move != '--':
                    # # print in commond line
                    # print '1 ' + str(ord(black_move[0]) - 97) + ' ' + str(8 - int(black_move[1]))

                    # convert and write in destination file
                    # outputfile.write('1 ' + str(ord(black_move[0]) - 97) + ' ' +
                    #                  str(8 - int(black_move[1]))+'\n')
                    outputfile.write('1 ' + str(ord(black_move[0]) - 97) + ' ' +
                                     str(8 - int(black_move[1])) + ' ' + str(black_score) + '\n')

                # if the line have only the first half of the record, just skip this turn
                # this usually means this is the last line of the record
                if len(line) < 50:
                    continue

                # read one turn of white
                white_cnt, white_move, white_score_s = line[38:40], line[42:44], line[45:52]

                # handle white_score
                if white_score_s.strip():
                    if white_score_s == 'Win    ':
                        white_score = 64
                    elif white_score_s == 'Loss   ':
                        white_score = -64
                    elif white_score_s == 'Draw   ':
                        white_score = 0
                    else:
                        white_score = float(white_score_s)
                else:
                    white_score = white_standard


                # if the white move is not forced to be skiped
                if white_move != '--':
                    # # print in commond line
                    # print '0 ' + str(ord(white_move[0]) - 97) + ' ' + str(8 - int(white_move[1]))

                    # convert and write in destination file
                    # outputfile.write('0 ' + str(ord(white_move[0]) - 97) + ' ' +
                    #                  str(8 - int(white_move[1]))+'\n')
                    outputfile.write('0 ' + str(ord(white_move[0]) - 97) + ' ' +
                                     str(8 - int(white_move[1])) + ' ' + str(white_score) + '\n')

        # close the file after reading or writing
        inputfile.close()
        outputfile.close()

    except Exception as msg:
        print("Error at \"" + filename +"\": ")
        print(msg)
        print('Continue...')
        inputfile.close()
        outputfile.close()
        os.unlink(outputfile.name)

    else:
        FILE_CNT += 1

# finish
print('File convertion finished: ')
RUNNING_TIME = round(time.time() - START_TIME, 3)
print("\tTotal running time: " + str(RUNNING_TIME) + " seconds.")
print("\t" + str(FILE_CNT) + " file(s) converted.")
