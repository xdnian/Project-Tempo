from othello import othello_engine as oe
import numpy as np
from keras.models import load_model
from keras.models import Sequential
from heuristic import CNN_CAT_heuristic as CNCH
from random import choice

DEPTH = 0

class ai_bot(object):
    """
    This AI bot is a scretch for a simple AI based on the move prediction.
    """
    def __init__(self, show = False, record = False, player = 1, depth=2):
        if player == 1 or player.lower() == "black":
            self.player = 1
        else:
            self.player = 0
        self.game_engine = oe(show = show, record = record)
        self.heuristic = CNCH('./model/CNN_cat_model_L_500.h5')
        self.infinite = 1000
        self.depth = depth

    def restart(self):
        self.game_engine.restart()

    def get_engine(self):
        return self.game_engine

    def get_player(self):
        return self.player

    def run_best_move(self):
        self.game_engine.set_show(False)
        (x, y) = self.get_best_move()
        ###DEBUG
        self.game_engine.set_show(True)
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
            flips = list(self.game_engine.get_last_flips())
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
        if str(self.heuristic) == 'Random':
            depth = 0
        if depth == 0:
            ###DEBUG
            # self.game_engine.set_show(True)
            # self.game_engine.display()
            ###DEBUG
            return self.heuristic.evaluate(self.game_engine, currentplayer)
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
            flips = list(self.game_engine.get_last_flips())
            result = -self.alpha_beta(player, depth - 1, -beta, -alpha)
            self.game_engine.undo_move(x, y, flips)
            if result >= beta:
                return beta
            if result > alpha:
                alpha = result
        return alpha



if __name__ == '__main__':
    cmd = raw_input("Start a new Game (y/n)? : ")
    bot = ai_bot(show = True, depth=DEPTH)
    while cmd == "y" or cmd == "Y":
        bot.get_engine().restart()
        cmd = raw_input("You want black(1)/white(0)? (default is black): ")
        if cmd == "0" or cmd.lower() == "white":
            bot.set_player(0)
        while not bot.get_engine().finished():
            if bot.get_engine().get_currentplayer(number = True) == bot.get_player():
                print "Your turn:", bot.get_engine().get_currentplayer(number = False)
                cmd = raw_input("input x y: ")
                if len(cmd) > 2:
                    if cmd[0].isdigit() and cmd[2].isdigit():
                        bot.get_engine().update(ord(cmd[0]) - ord('0'), ord(cmd[2]) - ord('0'))
            else:
                (x,y) = bot.run_best_move()
                print "The bot play on", x, y

        if bot.get_engine().get_winner() == 1:
            print "Winner is Black!"
        elif bot.get_engine().get_winner() == 0:
            print "Winner is White!"
        else:
            print "Draw!"
        print bot.get_engine().get_stones(player=1),":",bot.get_engine().get_stones(player=0)
        cmd = raw_input("Start a new Game (y/n)? : ")
