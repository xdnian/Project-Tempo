# -*- coding: utf-8 -*-
"""
numerical training set generator
"""
import os
import sys
import numpy as np
from othello import othello_engine as oe

class generator(object):
    """
    This class intend to generate the data for training from the existing file
    """

    def __init__(self, dirname):
        self.dirname = dirname
        self.oe = oe()

    def get_generate_data(self):
        print("Generate data start...")
        files = os.listdir(self.dirname)
        length = 0
        for filename in files:
            length += sum(1 for line in open(self.dirname + "/" + filename, "r"))
        data = np.empty((length, 9, 8, 8), dtype="int8")
        label = np.empty((length), dtype="float32")
        print("Total sample count: " + str(length))
        print("\nReading from " + self.dirname + ":")
        data_id = 0
        for filename in files:
            with open(self.dirname + "/" + filename, "r") as f:
                self.oe.restart()
                for line in f:
                    currentplayer = int(line[0])
                    x = int(line[2])
                    y = int(line[4])
                    score = float(line[6:])
                    if self.oe.get_currentplayer() == currentplayer:
                        if not self.oe.update(x, y):
                            print("Fatal error")
                            return
                        player = self.oe.get_currentplayer()
                        gameboard = self.oe.get_board()
                        validboards = self.oe.get_validboard(return_all=True)
                        arr = np.empty((9, 8, 8), dtype="int8")
                        for i in range(8):
                            for j in range(8):
                                if gameboard[i][j] == player:
                                    arr[0][i][j] = 1
                                    arr[1][i][j] = 1
                                    arr[2][i][j] = 0
                                elif gameboard[i][j] == 1 - player:
                                    arr[0][i][j] = -1
                                    arr[1][i][j] = 0
                                    arr[2][i][j] = 1
                                else:
                                    arr[0][i][j] = 0
                                    arr[1][i][j] = 0
                                    arr[2][i][j] = 0
                                if validboards[player][i][j] == player:
                                    arr[3][i][j] = 1
                                else:
                                    arr[3][i][j] = 0
                                if validboards[1-player][i][j] == 1-player:
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
                        label[data_id] = -score
                    else:
                        print currentplayer, self.oe.get_currentplayer()
                        print("Fatal error")
                        return

                    # progress report
                    percentage = round((float(data_id)/(length-1))*100, 1)
                    progress_bar = '#'*int(percentage/2)
                    sys.stdout.write(' ' + str(percentage) + '%  ||' + progress_bar +'->'+"\r")
                    sys.stdout.flush()

                    data_id += 1

        print "\nDeduplicating:"
        distinct_data = []
        distinct_label = []
        for i in range(length):
            if data[i].tolist() not in distinct_data:
                distinct_data.append(data[i].tolist())
                distinct_label.append(label[i])

            percentage = round((float(i)/(length-1))*100, 1)
            progress_bar = '#'*int(percentage/2)
            sys.stdout.write(' ' + str(percentage) + '%  ||' + progress_bar +'->'+"\r")
            sys.stdout.flush()

        print("\nOver!")
        print("Total sample count: " + str(len(distinct_data)))
        return np.array(distinct_data), np.array(distinct_label)

    def check_adjacent(self, i, j, board):
        for n in [-1, 1]:
            if i+n < 8 and i+n > -1:
                if board[i+n][j] == -1:
                    return True
            if j+n < 8 and j+n > -1:
                if board[i][j+n] == -1:
                    return True
        return False
