# -*- coding: utf-8 -*-
"""
catagorical training set generator
"""
import os
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
                                        arr[9][i][j] = 100
                                    else:
                                        arr[9][i][j] = 0
                                    arr[10][i][j] = 100
                                    if gameboard[i][j] == 1:
                                        arr[1][i][j] = 100
                                        arr[2][i][j] = 100
                                        arr[3][i][j] = 0
                                    elif gameboard[i][j] == 0:
                                        arr[1][i][j] = 100
                                        arr[2][i][j] = 0
                                        arr[3][i][j] = 100
                                    else:
                                        arr[1][i][j] = 0
                                        arr[2][i][j] = 0
                                        arr[3][i][j] = 0
                                    if validboards[player][i][j] == player:
                                        arr[4][i][j] = 100
                                    else:
                                        arr[4][i][j] = 0
                                    if gameboard[i][j] == -1:
                                        arr[5][i][j] = 0
                                        arr[6][i][j] = 0
                                        arr[7][i][j] = 0
                                        arr[8][i][j] = 0
                                    elif self.check_adjacent(i, j, gameboard):
                                        if gameboard[i][j] == 1:
                                            arr[5][i][j] = 100
                                            arr[6][i][j] = 0
                                            arr[7][i][j] = 0
                                            arr[8][i][j] = 0
                                        elif gameboard[i][j] == 0:
                                            arr[5][i][j] = 0
                                            arr[6][i][j] = 0
                                            arr[7][i][j] = 100
                                            arr[8][i][j] = 0
                                    else:
                                        if gameboard[i][j] == 1:
                                            arr[5][i][j] = 0
                                            arr[6][i][j] = 100
                                            arr[7][i][j] = 0
                                            arr[8][i][j] = 0
                                        elif gameboard[i][j] == 0:
                                            arr[5][i][j] = 0
                                            arr[6][i][j] = 0
                                            arr[7][i][j] = 0
                                            arr[8][i][j] = 100

                            data[data_id, :, :, :] = arr
                            label[data_id] = score if currentplayer == 1 else -score
                            data_id += 1
                    else:
                        print currentplayer, self.oe.get_currentplayer()
                        print("Fatal error")
                        return

        print "Over!"
        return data, label

    def check_adjacent(self, i, j, board):
        for n in [-1, 1]:
            if i+n < 8 and i+n > -1:
                if board[i+n][j] == -1:
                    return True
            if j+n < 8 and j+n > -1:
                if board[i][j+n] == -1:
                    return True
        return False
