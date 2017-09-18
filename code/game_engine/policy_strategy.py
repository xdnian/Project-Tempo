import time
import numpy as np
from keras.models import load_model, Sequential
from utils import Othello
import utils

LABEL_MAP = [11, 12, 13, 14, 15, 16, 17, 18,
             21, 22, 23, 24, 25, 26, 27, 28,
             31, 32, 33, 34, 35, 36, 37, 38,
             41, 42, 43, 44, 45, 46, 47, 48,
             51, 52, 53, 54, 55, 56, 57, 58,
             61, 62, 63, 64, 65, 66, 67, 68,
             71, 72, 73, 74, 75, 76, 77, 78,
             81, 82, 83, 84, 85, 86, 87, 88,]

# model = load_model("CNN_cat_model_L_500.h5")
model = None
cnn_time = 0
cnn_cnt = 0


def load(path):
    global model
    if path == None:
        return
    model = load_model(path)
    print 'Model loaded'

def check_adjacent(square, board):
    for d in utils.DIRECTIONS4:
        if board[square + d] == utils.EMPTY:
            return True
    return False

def get_move(player, board):
    data = np.empty((1, 10, 8, 8), dtype="int8")
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

    data[0] = arr
    # print utils.print_board(board)
    # print arr
    # raw_input()

    prob = model.predict(data, batch_size=1)[0]
    # prob = np.reshape(prob, 64)

    validpred = np.asarray(list([i, prob[LABEL_MAP.index(i)]] for i in validmoves))
    move = validpred[np.argmax(validpred[:,1])][0]
    return int(move)
