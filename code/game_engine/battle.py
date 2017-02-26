from othello import othello_engine as oe
from random import choice
import copy as cp
from heuristic import simple_heuristic as SH
from heuristic import CNN_heuristic as CNNH
from heuristic import MLP_heuristic as MLPH
from heuristic import random_heuristic as RANH
from heuristic import MLP_CAT_heuristic as MLCH
from heuristic import CNN_CAT_heuristic as CNCH

class battle_bot(object):
    '''
    This class is for the battle between AIs. The first heuristic is for the white, the second is for the black.
    '''
    def __init__(self, show = False, record = False, heuristic = [], depth = 2, infinite = 1000):
        if heuristic == []:
            self.heuristic = [SH(), SH()]
        else:
            self.heuristic = heuristic
        self.depth = depth
        self.infinite = infinite
        self.game_engine = oe(show = show, record = record)

    def restart(self):
        self.game_engine.restart()

    def get_engine(self):
        return self.game_engine

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def run_best_move(self):
        self.game_engine.set_show(False)
        (x, y) = self.get_best_move()
        ###DEBUG
        # self.game_engine.set_show(True)
        ###DEBUG
        self.game_engine.update(x, y)
        return (x, y)

    def get_best_move(self):
        currentplayer = self.game_engine.get_currentplayer()
        bestmove = []
        bestresult = -self.infinite
        moves = self.get_ordered_moves(self.game_engine, currentplayer)
        if len(moves) == 0:
            print "No Valid moves"
            return None
        for x, y in moves:
            self.game_engine.update(x, y)
            flips = cp.deepcopy(self.game_engine.get_last_flips())
            result = -self.alpha_beta(currentplayer, self.depth, bestresult, self.infinite)
            self.game_engine.undo_move(x, y, flips)
            if result > bestresult:
                bestresult = result
                bestmove = [(x, y)]
            elif result == bestresult:
                bestmove.append((x, y))
        return choice(bestmove)

    def get_ordered_moves(self, engine, player):
        moves = []
        if engine.get_validmoves(player = player) == 0:
            return moves
        validboard = engine.get_validboard(player = player)
        for x, y in [(0,0),(0,7),(7,0),(7,7)]:
            if validboard[x][y] == player:
                moves.append((x,y))
        for x in [0,7]:
            for y in range(8)[1:-1]:
                if validboard[x][y] == player:
                    moves.append((x,y))
                if validboard[y][x] == player:
                    moves.append((y,x))
        for x in range(8)[1:-1]:
            for y in range(8)[1:-1]:
                if validboard[x][y] == player:
                    moves.append((x,y))
        return moves

    def alpha_beta(self, player, depth, alpha, beta):
        currentplayer = self.game_engine.get_currentplayer()
        if depth == 0:
            ###DEBUG
            # self.game_engine.set_show(True)
            # self.game_engine.display()
            ###DEBUG
            return self.heuristic[player].evaluate(self.game_engine, currentplayer)
        if self.game_engine.finished():
            if self.game_engine.get_winner() == currentplayer:
                return -self.infinite
            elif self.game_engine.get_winner() == 1-currentplayer:
                return self.infinite
            else:
                return 0
        moves = self.get_ordered_moves(self.game_engine, currentplayer)
        if len(moves) == 0:
            result = -self.alpha_beta(player, depth - 1, -beta, -alpha)
            if result >= beta:
                return beta
            else:
                return max(alpha, result)
        for x, y in moves:
            self.game_engine.update(x, y)
            flips = cp.deepcopy(self.game_engine.get_last_flips())
            result = -self.alpha_beta(player, depth - 1, -beta, -alpha)
            self.game_engine.undo_move(x, y, flips)
            if result >= beta:
                return beta
            if result > alpha:
                alpha = result
        return alpha

    def loop(self, iterations, count):
        k = 0
        sum_black = 0
        sum_white = 0
        draw = 0
        for i in xrange(iterations):
            if k >= count:
                k = 0
                print "Black wins:", sum_black, "/", i, ", winning rate =", sum_black*1.0/i
                print "White wins:", sum_white, "/", i, ", winning rate =", sum_white*1.0/i
                print "Draw:", draw, "/", i, "draw rate =", draw*1.0/i
            self.restart()
            while not self.game_engine.finished():
                self.run_best_move()
            if self.game_engine.get_winner() == 1:
                sum_black += 1
            elif self.game_engine.get_winner() == 0:
                sum_white += 1
            elif self.game_engine.get_winner() == -1:
                draw += 1
            k+=1

        print "Black wins:", sum_black, "/", iterations, ", winning rate =", sum_black*1.0/iterations
        print "White wins:", sum_white, "/", iterations, ", winning rate =", sum_white*1.0/iterations
        print "Draw:", draw, "/", iterations, "draw rate =", draw*1.0/iterations

# model = MLPH(model = "MLP_score_model.h5")
# model = CNNH(model = "CNN_score_model.h5")
# model = MLCH(model = "MLP_cat_model.h5")
# model = CNCH(model = "CNN_cat_model.h5")
model = CNCH(model = "CNN_cat_large_model.h5")
# battle = battle_bot(depth=0, heuristic=[model, SH()])
battle = battle_bot(depth=0, heuristic=[SH(), model])
# battle = battle_bot(depth=0, heuristic=[RANH(), model])
# battle = battle_bot(depth=1, heuristic=[SH(), RANH()])
# battle = battle_bot(depth=0, heuristic=[model, RANH()])
# battle = battle_bot(depth=0, heuristic=[RANH(), RANH()])



battle.loop(100,10)
#
# battle = battle_bot(depth=0, heuristic=[model, RANH()])
# battle.loop(250,10)
