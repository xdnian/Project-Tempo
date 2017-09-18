# -*- coding: utf-8 -*-
"""
value network training set generator
"""
import os
import sys
import numpy as np
from utils import Othello
import utils


class generator(object):
    """
    This class intend to generate the data for training from the existing file
    """

    def __init__(self, dirname):
        self.dirname = dirname

    def get_generate_data(self):
        print ("start")
        files = os.listdir(self.dirname)
        length = 0
        for filename in files:
            length += sum(1 for line in open(self.dirname + "/" + filename, "r"))
        length*=4
        print length
        data = np.empty((length, 10, 8, 8), dtype="int8")
        label = np.empty(length, dtype="float32, int32")
        data_id = 0
        for filename in files:
            with open(self.dirname + "/" + filename, "r") as f:
                for line in f:
                    # Read the board, player and Q/N from the file
                    board, player = Othello.str_to_board(line[0:102])
                    values = line[103:].split(' ')
                    Q = float(values[0])
                    N = int(values[1])

                    # Process the board into training data
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

                    label[data_id:data_id+4] = [(Q, N)]*4

                    # progress report
                    percentage = int((float(data_id+1) / (length)) * 30)
                    progress_bar = '[' + '='*percentage + '>' + '.'*(29-percentage) + ']'
                    sys.stdout.write(' ' + str(data_id+1) + '/' + str(length) + ' ' + progress_bar + '\r')
                    sys.stdout.flush()

                    data_id += 4


        #Map
        print ("\nMap:")
        bin_board_dict = {}
        for i in xrange(length):
            key = int(
                ''.join(list(str(num) for own_stone_list in data[i][1].tolist() for num in own_stone_list))
                + ''.join(list(str(num) for oppo_stone_list in data[i][2].tolist() for num in oppo_stone_list)),
                2)
            if label[i][1] > 10:
                if key not in bin_board_dict:
                    bin_board_dict[key] = []
                bin_board_dict[key].append(i)

            # progress report
            percentage = int((float(i+1) / (length)) * 30)
            progress_bar = '[' + '='*percentage + '>' + '.'*(29-percentage) + ']'
            sys.stdout.write(' ' + str(i+1) + '/' + str(length) + ' ' + progress_bar + '\r')
            sys.stdout.flush()

        #Reduce
        print ("\nReduce")
        uni_length = len(bin_board_dict)
        uni_data = np.empty((uni_length, 10, 8, 8), dtype="int8")
        uni_label = np.zeros(uni_length, dtype="float32")
        uni_data_id = 0
        print(uni_length)
        for board in bin_board_dict:
            uni_data[uni_data_id] = data[bin_board_dict[board][0]]
            uni_label[uni_data_id] = sum(inner_product(label[i]) for i in bin_board_dict[board])/sum(label[i][1] for i in bin_board_dict[board])

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

def inner_product(a):
    return a[0]*a[1]

if __name__ == '__main__':
    ge = generator("./mcts_results/random")
    data, label = ge.get_generate_data()
    f = file("./dataset/random_value_training_data.npy", "wb")
    np.save(f, data)
    np.save(f, label)
    f.close()
