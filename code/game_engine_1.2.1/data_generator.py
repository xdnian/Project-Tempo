# -*- coding: utf-8 -*-
"""
policy network training set generator
"""
import os
import sys
import numpy as np
from othello import othello_engine as oe

BORDER = np.ones((10, 10), dtype="int8")
for i in range(1,9):
    for j in range(1,9):
        BORDER[i][j] = 0
# print BORDER
LABEL_MAP = [[ 0,  1,  2,    3,    4,  5,  6,  7],
             [ 8,  9, 10,   11,   12, 13, 14, 15],
             [16, 17, 18,   19,   20, 21, 22, 23],
             [24, 25, 26, None, None, 27, 28, 29],
             [30, 31, 32, None, None, 33, 34, 35],
             [36, 37, 38,   39,   40, 41, 42, 43],
             [44, 45, 46,   47,   48, 49, 50, 51],
             [52, 53, 54,   55,   56, 57, 58, 59]]

class generator(object):
    """
    This class intend to generate the data for training from the existing file
    """

    def __init__(self, dirname, omit_lines=0):
        self.dirname = dirname
        self.oe = oe()
        self.omit_lines = omit_lines

    def get_generate_data(self):
        print "start"
        files = os.listdir(self.dirname)
        length = 0
        for filename in files:
            # if sum(1 for line in open(self.dirname + "/" + filename, "r")) < self.omit_lines:
            #     print "ERROR\n",filename
            length += sum(1 for line in open(self.dirname + "/" + filename, "r")) - self.omit_lines
        length*=4
        print length
        data = np.empty((length, 11, 10, 10), dtype="int8")
        label = np.empty((length, 2), dtype="float32")
        data_id = 0
        for filename in files:
            with open(self.dirname + "/" + filename, "r") as f:
                self.oe.restart()
                line_count = 0
                for line in f:
                    line_count += 1
                    currentplayer = int(line[0])
                    x = int(line[2])
                    y = int(line[4])
                    score = float(line[6:])
                    if self.oe.get_currentplayer() == currentplayer:
                        if line_count > self.omit_lines:
                            player = self.oe.get_currentplayer()
                            gameboard = self.oe.get_board()
                            validboards = self.oe.get_validboard(return_all=True)
                            arr = np.zeros((11, 10, 10), dtype="int8")
                            arr[10] = np.ones((10, 10), dtype="int8")
                            arr[9] = BORDER
                            for i in range(1,9):
                                for j in range(1,9):
                                    i_board = i-1
                                    j_board = j-1
                                    if gameboard[i_board][j_board] == player:
                                        arr[1][i][j] = 1
                                    elif gameboard[i_board][j_board] == 1-player:
                                        arr[2][i][j] = 1
                                    else:
                                        arr[3][i][j] = 1
                                    if validboards[player][i_board][j_board] == player:
                                        arr[4][i][j] = 1
                                    if gameboard[i_board][j_board] != -1:
                                        if self.check_adjacent(i_board, j_board, gameboard):
                                            if gameboard[i_board][j_board] == player:
                                                arr[5][i][j] = 1
                                            elif gameboard[i_board][j_board] == 1-player:
                                                arr[7][i][j] = 1
                                        else:
                                            if gameboard[i_board][j_board] == player:
                                                arr[6][i][j] = 1
                                            elif gameboard[i_board][j_board] == 1-player:
                                                arr[8][i][j] = 1

                            data[data_id, :, :, :] = arr
                            data[data_id+1, :, :, :] = np.array(list(m.transpose() for m in arr))
                            arr = arr[:,::-1,::-1]
                            data[data_id+2, :, :, :] = arr
                            data[data_id+3, :, :, :] = np.array(list(m.transpose() for m in arr))

                            label[data_id][0] = LABEL_MAP[x][y]
                            label[data_id+1][0] = LABEL_MAP[y][x]
                            label[data_id+2][0] = LABEL_MAP[7-x][7-y]
                            label[data_id+3][0] = LABEL_MAP[7-y][7-x]

                            label[data_id][1] = score
                            label[data_id+1][1] = score
                            label[data_id+2][1] = score
                            label[data_id+3][1] = score


                            # progress report
                            percentage = round((float(data_id)/(length-1))*100, 1)
                            progress_bar = '#'*int(percentage/2)
                            sys.stdout.write(' ' + str(percentage) + '%  ||' + progress_bar +'->'+"\r")
                            sys.stdout.flush()

                            data_id += 4

                        if not self.oe.update(x, y):
                            print("Fatal error")
                            return
                    else:
                        print currentplayer, self.oe.get_currentplayer()
                        print("Fatal error")
                        return

        print "\nDeduplicating:"
        #Map
        bin_board_dict = {}
        for i in xrange(length):
            key = int(
                ''.join(list(str(num) for own_stone_list in data[i][1].tolist() for num in own_stone_list))
                + ''.join(list(str(num) for oppo_stone_list in data[i][2].tolist() for num in oppo_stone_list)))
            if key not in bin_board_dict:
                bin_board_dict[key] = [i]
            bin_board_dict[key].append(i)

        #Reduce
        uni_length = len(bin_board_dict)
        uni_data = np.empty((uni_length, 11, 10, 10), dtype="int8")
        uni_label = np.empty(uni_length, dtype="int8")
        uni_data_id = 0
        for board in bin_board_dict:
            uni_data[uni_data_id] = data[bin_board_dict[board][0]]
            temp_label = np.asarray(list(label[i] for i in bin_board_dict[board]))
            uni_label[uni_data_id] = int(temp_label[np.argmax(temp_label[:,1])][0])

            percentage = round((float(uni_data_id)/(uni_length-1))*100, 1)
            progress_bar = '#'*int(percentage/2)
            sys.stdout.write(' ' + str(percentage) + '%  ||' + progress_bar +'->'+"\r")
            sys.stdout.flush()

            uni_data_id += 1

        print("\nOver!")
        print("Total sample count: " + str(len(uni_data)))
        return uni_data, uni_label

    def check_adjacent(self, i, j, board):
        for n in [-1, 1]:
            if i+n < 8 and i+n > -1:
                if board[i+n][j] == -1:
                    return True
            if j+n < 8 and j+n > -1:
                if board[i][j+n] == -1:
                    return True
        return False


if __name__ == '__main__':
    ge = generator("../../training_set/DEST_SCORE", 0)
    data, label = ge.get_generate_data()
    f = file("p_training_set_10_L.npy", "wb")
    np.save(f, data)
    np.save(f, label)
    f.close()
