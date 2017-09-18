import time
import math
import numpy as np
from keras.models import load_model, Sequential
from utils import Othello
import utils

class ValueNetwork(object):
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

        score = self.model.predict(data, batch_size=1)[0]

        return score
