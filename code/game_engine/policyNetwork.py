import time
import math
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

# softmax temperature
T = 1

class PolicyNetwork(object):
    def __init__(self, model=None):
        self.model = None
        self.load_model(model)

    def load_model(self, path):
        if path == None:
            return
        self.model = load_model(path)
        print 'Model loaded'

    def check_adjacent(self, square, board):
        for d in utils.DIRECTIONS4:
            if board[square + d] == utils.EMPTY:
                return True
        return False

    def evaluate(self, game):

        # player = utils.PIECES.index(player) # black-1, white-0
        data = np.empty((1, 10, 8, 8), dtype="int8")
        player = game.player
        board = game.board
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
                    if self.check_adjacent(square, board):
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

        prob = self.model.predict(data, batch_size=1)[0]
        prob = np.reshape(prob, 64)

        # softmax temperature manipulate
        prob_sum = 0
        for i in validmoves:
            prob[LABEL_MAP.index(i)] = math.exp(prob[LABEL_MAP.index(i)]/T)
            prob_sum += prob[LABEL_MAP.index(i)]

        move_probs = list((i, prob[LABEL_MAP.index(i)]/prob_sum) for i in validmoves)

        return move_probs
