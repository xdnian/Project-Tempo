import time
import numpy as np
import random
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

class RandomNetwork(object):
    def evaluate(self, game):
        player = game.player
        board = game.board
        validmoves = Othello.legal_moves(player, board)
        if len(validmoves) == 0:
            return []
        prob = 1.0 / len(validmoves)
        random.shuffle(validmoves)
        move_probs = list((i, prob) for i in validmoves)
        return move_probs
