# -*- coding: utf-8 -*-
"""
catagorical training set generator
"""
import os
import sys
import numpy as np
from othello import othello_engine as oe

class generator(object):
    """
    This class intend to generate the data for training from the existing file
    """

    def __init__(self, dirname, omit_lines=8):
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
        data = np.empty((length, 11, 8, 8), dtype="int8")
        label = np.empty((length), dtype="int8")
        print length
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
                    score = int(line[6:])
                    if self.oe.get_currentplayer() == currentplayer:
                        if not self.oe.update(x, y):
                            print("Fatal error")
                            return
                        if line_count > self.omit_lines:
                            player = self.oe.get_currentplayer()
                            gameboard = self.oe.get_board()
                            validboards = self.oe.get_validboard(return_all=True)
                            arr = np.empty((11, 8, 8), dtype="int8")
                            for i in range(8):
                                for j in range(8):
                                    arr[0][i][j] = 0
                                    if i==0 or i==7 or j==0 or j==7:
                                        arr[9][i][j] = 1
                                    else:
                                        arr[9][i][j] = 0
                                    arr[10][i][j] = 1
                                    if gameboard[i][j] == player:
                                        arr[1][i][j] = 1
                                        arr[2][i][j] = 0
                                        arr[3][i][j] = 0
                                    elif gameboard[i][j] == 1-player:
                                        arr[1][i][j] = 0
                                        arr[2][i][j] = 1
                                        arr[3][i][j] = 0
                                    else:
                                        arr[1][i][j] = 0
                                        arr[2][i][j] = 0
                                        arr[3][i][j] = 1
                                    if validboards[player][i][j] == player:
                                        arr[4][i][j] = 1
                                    else:
                                        arr[4][i][j] = 0
                                    if gameboard[i][j] == -1:
                                        arr[5][i][j] = 0
                                        arr[6][i][j] = 0
                                        arr[7][i][j] = 0
                                        arr[8][i][j] = 0
                                    elif self.check_adjacent(i, j, gameboard):
                                        if gameboard[i][j] == player:
                                            arr[5][i][j] = 1
                                            arr[6][i][j] = 0
                                            arr[7][i][j] = 0
                                            arr[8][i][j] = 0
                                        elif gameboard[i][j] == 1-player:
                                            arr[5][i][j] = 0
                                            arr[6][i][j] = 0
                                            arr[7][i][j] = 1
                                            arr[8][i][j] = 0
                                    else:
                                        if gameboard[i][j] == player:
                                            arr[5][i][j] = 0
                                            arr[6][i][j] = 1
                                            arr[7][i][j] = 0
                                            arr[8][i][j] = 0
                                        elif gameboard[i][j] == 1-player:
                                            arr[5][i][j] = 0
                                            arr[6][i][j] = 0
                                            arr[7][i][j] = 0
                                            arr[8][i][j] = 1

                            data[data_id, :, :, :] = arr
                            data[data_id+1, :, :, :] = np.array(list(m.transpose() for m in arr))
                            arr = arr[:,::-1,::-1]
                            data[data_id+2, :, :, :] = arr
                            data[data_id+3, :, :, :] = np.array(list(m.transpose() for m in arr))
                            label[data_id:data_id+4] = [score]*4 #if currentplayer == 1 else -score

                            # progress report
                            percentage = round((float(data_id)/(length-1))*100, 1)
                            progress_bar = '#'*int(percentage/2)
                            sys.stdout.write(' ' + str(percentage) + '%  ||' + progress_bar +'->'+"\r")
                            sys.stdout.flush()

                            data_id += 4
                    else:
                        print currentplayer, self.oe.get_currentplayer()
                        print("Fatal error")
                        return

        #Map
        print "\nDeduplicating:"
        bin_board_dict = {}
        for i in xrange(length):
            key = int(
                ''.join(list(str(num) for own_stone_list in data[i][1].tolist() for num in own_stone_list))
                + ''.join(list(str(num) for oppo_stone_list in data[i][2].tolist() for num in oppo_stone_list))
                )
            if key not in bin_board_dict:
                bin_board_dict[key] = []
            bin_board_dict[key].append(i)

        #Reduce
        uni_length = len(bin_board_dict)
        uni_data = np.empty((uni_length, 11, 8, 8), dtype="int8")
        uni_label = np.empty(uni_length, dtype="int8")
        uni_data_id = 0
        for board in bin_board_dict:
            uni_data[uni_data_id] = data[bin_board_dict[board][0]]
            uni_label[uni_data_id] = int(sum(label[i] for i in bin_board_dict[board])/len(bin_board_dict[board]))

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
    ge = generator("../../trainning_set/DEST_CAT", 0)
    data, label = ge.get_generate_data()
    f = file("training.npy", "wb")
    np.save(f, data)
    np.save(f, label)
    f.close()
