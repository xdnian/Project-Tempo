# -*- coding: utf-8 -*-
"""
policy network training set generator
"""
import os
import sys
import numpy as np
from utils import Othello
import utils

LABEL_MAP = list(list(i + j*8 for i in range(8))for j in range(8))


class generator(object):
    """
    This class intend to generate the data for training from the existing file
    """

    def __init__(self, dirname, omit_lines=8):
        self.dirname = dirname
        self.game = Othello()
        self.omit_lines = omit_lines

    def get_generate_data(self):
        print ("start")
        files = os.listdir(self.dirname)
        length = 0
        for filename in files:
            # if sum(1 for line in open(self.dirname + "/" + filename, "r")) < self.omit_lines:
            #     print "ERROR\n",filename
            length += sum(1 for line in open(self.dirname + "/" + filename, "r")) - self.omit_lines
        length*=4
        print length
        data = np.empty((length, 10, 8, 8), dtype="int8")
        label = np.empty((length), dtype="int8")
        data_id = 0
        for filename in files:
            with open(self.dirname + "/" + filename, "r") as f:
                self.game.restart()
                line_count = 0
                for line in f:
                    line_count += 1
                    currentplayer = utils.PIECES[int(line[0])]
                    x = int(line[2])
                    y = int(line[4])
                    # score = float(line[6:])
                    if self.game.player == currentplayer:
                        if line_count > self.omit_lines:
                            player = self.game.player
                            board = self.game.board
                            validmoves = Othello.legal_moves(player, board)
                            arr = np.zeros((10, 8, 8), dtype="int8")
                            arr[9] = np.ones((8, 8), dtype="int8")

                            for i in xrange(8):
                                for j in xrange(8):
                                    square = i + j*10 + 11
                                    if square in validmoves:
                                        arr[4][i][j] = 1
                                    if board[square] == utils.EMPTY:
                                        arr[3][i][j] = 1
                                    else:
                                        if board[square] == player:
                                            arr[1][i][j] = 1
                                        elif board[square] == Othello.opponent(player):
                                            arr[2][i][j] = 1
                                        if check_adjacent(square, board):
                                            if board[square] == player:
                                                arr[5][i][j] = 1
                                            elif board[square] == Othello.opponent(player):
                                                arr[7][i][j] = 1
                                        else:
                                            if board[square] == player:
                                                arr[6][i][j] = 1
                                            elif board[square] == Othello.opponent(player):
                                                arr[8][i][j] = 1


                            data[data_id, :, :, :] = arr
                            data[data_id+1, :, :, :] = np.array(list(m.transpose() for m in arr))
                            arr = arr[:,::-1,::-1]
                            data[data_id+2, :, :, :] = arr
                            data[data_id+3, :, :, :] = np.array(list(m.transpose() for m in arr))

                            label[data_id] = LABEL_MAP[x][y]
                            label[data_id+1] = LABEL_MAP[y][x]
                            label[data_id+2] = LABEL_MAP[7-x][7-y]
                            label[data_id+3] = LABEL_MAP[7-y][7-x]

                            # progress report
                            percentage = int((float(data_id+1) / (length)) * 30)
                            progress_bar = '[' + '='*percentage + '>' + '.'*(29-percentage) + ']'
                            sys.stdout.write(' ' + str(data_id+1) + '/' + str(length) + ' ' + progress_bar + '\r')
                            sys.stdout.flush()

                            data_id += 4

                    pos = x + y*10 + 11
                    self.game.make_valid_move(pos)

        #Map
        print ("\nMap:")
        bin_board_dict = {}
        for i in xrange(length):
            key = int(
                ''.join(list(str(num) for own_stone_list in data[i][1].tolist() for num in own_stone_list))
                + ''.join(list(str(num) for oppo_stone_list in data[i][2].tolist() for num in oppo_stone_list))
                + bin(label[i])[2:], 2)
            if key not in bin_board_dict:
                bin_board_dict[key] = i

            # progress report
            percentage = int((float(i+1) / (length)) * 30)
            progress_bar = '[' + '='*percentage + '>' + '.'*(29-percentage) + ']'
            sys.stdout.write(' ' + str(i+1) + '/' + str(length) + ' ' + progress_bar + '\r')
            sys.stdout.flush()

        #Reduce
        print ("\nReduce")
        uni_length = len(bin_board_dict)
        uni_data = np.empty((uni_length, 10, 8, 8), dtype="int8")
        uni_label = np.zeros(uni_length, dtype="int8")
        uni_data_id = 0
        print(uni_length)
        for board in bin_board_dict:
            uni_data[uni_data_id] = data[bin_board_dict[board]]

            uni_label[uni_data_id] = label[bin_board_dict[board]]

            # progress report
            percentage = int((float(uni_data_id+1) / (uni_length)) * 30)
            progress_bar = '[' + '='*percentage + '>' + '.'*(29-percentage) + ']'
            sys.stdout.write(' ' + str(uni_data_id+1) + '/' + str(uni_length) + ' ' + progress_bar + '\r')
            sys.stdout.flush()

            uni_data_id += 1

        print("\nOver!")
        print("Total sample count: " + str(len(uni_data)))
        return uni_data, uni_label

def check_adjacent(square, board):
    for d in utils.DIRECTIONS4:
        if board[square + d] == utils.EMPTY:
            return True
    return False


if __name__ == '__main__':
    ge = generator("../../training_set/DEST_CAT", 0)
    data, label = ge.get_generate_data()
    f = file("./dataset/policy_training_data.npy", "wb")
    np.save(f, data)
    np.save(f, label)
    f.close()
