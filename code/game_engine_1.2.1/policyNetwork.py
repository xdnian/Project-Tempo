import time
import numpy as np
from keras.models import load_model, Sequential
from paip_othello_class_mcts import othello as Paip
import paip_othello_class_mcts as othello

# from paip_othello_class import othello as Paip
# import paip_othello_class as othello

LABEL_MAP = [11, 12, 13, 14, 15, 16, 17, 18,
             21, 22, 23, 24, 25, 26, 27, 28,
             31, 32, 33, 34, 35, 36, 37, 38,
             41, 42, 43,         46, 47, 48,
             51, 52, 53,         56, 57, 58,
             61, 62, 63, 64, 65, 66, 67, 68,
             71, 72, 73, 74, 75, 76, 77, 78,
             81, 82, 83, 84, 85, 86, 87, 88,]

# model = load_model("CNN_cat_model_L_500.h5")
model = None
cnn_time = 0
cnn_cnt = 0

BORDER = np.ones((10, 10), dtype="int8")
for i in range(1,9):
    for j in range(1,9):
        BORDER[i][j] = 0

class PolicyNetwork(object):
    def __init__(self, model=None):
        self.model = None
        self.load_model(model)

    def load_model(self, path):
        if path == None:
            return
        # global model, cnn_time, cnn_cnt
        self.model = load_model(path)
        # cnn_time = 0
        # cnn_cnt = 0
        print 'Model loaded'

    def check_adjacent(self, square, board):
        for d in othello.DIRECTIONS4:
            if board[square + d] == othello.EMPTY:
                return True
        return False

    def evaluate(self, paip):
        # global cnn_time, cnn_cnt
        # start = time.time()
        # player = othello.PIECES.index(player) # black-1, white-0
        data = np.empty((1, 11, 10, 10), dtype="int8")
        player = paip.player
        board = paip.board
        # gameboard = list(board[i] for i in othello.squares())
        # gameboard = list(list(gameboard[i-m*8] for m in xrange(8)) for i in xrange(56, 64))
        validmoves = Paip.legal_moves(player, board)
        # validboard = list(int(i in validmoves) for i in othello.squares())
        # validboard = list(list(validboard[i-m*8] for m in xrange(8)) for i in xrange(56, 64))


        arr = np.zeros((11, 10, 10), dtype="int8")
        arr[10] = np.ones((10, 10), dtype="int8")
        arr[9] = BORDER

        for i in xrange(1,9):
            for j in xrange(1,9):
                square = i + j*10
                if square in validmoves:
                    arr[4][i][j] = 1
                if board[square] == othello.EMPTY:
                    arr[3][i][j] = 1
                else:
                    if board[square] == player:
                        arr[1][i][j] = 1
                    elif board[square] == Paip.opponent(player):
                        arr[2][i][j] = 1
                    if self.check_adjacent(square, board):
                        if board[square] == player:
                            arr[5][i][j] = 1
                        elif board[square] == Paip.opponent(player):
                            arr[7][i][j] = 1
                    else:
                        if board[square] == player:
                            arr[6][i][j] = 1
                        elif board[square] == Paip.opponent(player):
                            arr[8][i][j] = 1

        data[0] = arr
        # print othello.print_board(board)
        # print arr
        # raw_input()

        prob = self.model.predict(data, batch_size=1)[0]

        prob_sum = sum(prob[validmoves.index(i)] for i in validmoves)
        move_probs = list((i, prob[validmoves.index(i)]/prob_sum) for i in validmoves)

        # cnn_time += time.time()-start
        # cnn_cnt += 1

        return move_probs
