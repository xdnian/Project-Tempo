import time
import numpy as np
from keras.models import load_model, Sequential
import paip_othello_class as paip

# model = load_model("CNN_cat_model_L_500.h5")
model = None
cnn_time = 0
cnn_cnt = 0

def load(path):
    global model, cnn_time, cnn_cnt
    model = load_model(path)
    cnn_time = 0
    cnn_cnt = 0
    print 'Model loaded'

def check_adjacent(square, board):
    for d in paip.DIRECTIONS4:
        if board[square + d] == paip.EMPTY:
            return True
    return False

def CNN_strategy(player, board):
    global cnn_time, cnn_cnt
    start = time.time()
    # player = paip.PIECES.index(player) # black-1, white-0
    data = np.empty((1, 11, 8, 8), dtype="int8")

    # gameboard = list(board[i] for i in paip.squares())
    # gameboard = list(list(gameboard[i-m*8] for m in xrange(8)) for i in xrange(56, 64))
    validmoves = paip.othello.legal_moves(player, board)
    # validboard = list(int(i in validmoves) for i in paip.squares())
    # validboard = list(list(validboard[i-m*8] for m in xrange(8)) for i in xrange(56, 64))


    arr = np.zeros((11, 8, 8), dtype="int8")
    arr[10] = np.ones((8, 8), dtype="int8")

    for i in xrange(8):
        for j in xrange(8):
            square = i + j*10 + 11
            if i in (0, 7) or j in (0, 7):
                arr[9][i][j] = 1
            if square in validmoves:
                arr[4][i][j] = 1
            if board[square] == paip.EMPTY:
                arr[3][i][j] = 1
            else:
                if board[square] == player:
                    arr[1][i][j] = 1
                elif board[square] == paip.othello.opponent(player):
                    arr[2][i][j] = 1
                if check_adjacent(square, board):
                    if board[square] == player:
                        arr[5][i][j] = 1
                    elif board[square] == paip.othello.opponent(player):
                        arr[7][i][j] = 1
                else:
                    if board[square] == player:
                        arr[6][i][j] = 1
                    elif board[square] == paip.othello.opponent(player):
                        arr[8][i][j] = 1

    data[0] = arr
    # print paip.othello.print_board(board)
    # print arr
    # raw_input()

    cat = model.predict(data, batch_size=1)
    value = np.argmax(cat[0])
    if value > 8:
        value = value - 17
    cnn_time += time.time()-start
    cnn_cnt += 1

    return -value
