from othello import othello_engine as oe
from random import choice
import copy as cp
from heuristic import simple_heuristic as SH
from heuristic import CNN_heuristic as CNNH

class AI_bot(object):
    """
    This AI bot use alpha beta search to do simple AI compute.
    It heuristic function can be
    1) a simple evalutation function by given points of certain pieces on corners and sides
    2) a more complex evaluation function
    3) a customed heuristic passed in
    """
    def __init__(self, show = False, record = False, player = 1, heuristic = None, depth = 2, infinite = 1000):
        if player == 1 or player.lower() == "black":
            self.player = 1
        else:
            self.player = 0
        if heuristic == None:
            self.heuristic = SH()
        else:
            self.heuristic = heuristic
        self.depth = depth
        self.infinite = infinite
        self.game_engine = oe(show = show, record = record)

    def restart(self):
        self.game_engine.restart()

    def get_engine(self):
        return self.game_engine

    def get_player(self):
        return self.player

    def set_player(self, player):
        if player == 1:
            self.player = 1
        else:
            self.player = 0

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def run_best_move(self):
        self.game_engine.set_show(False)
        (x, y) = self.get_best_move()
        self.game_engine.set_show(True)
        self.game_engine.update(x, y)
        return (x, y)

    def get_best_move(self):
        bestmove = []
        bestresult = -self.infinite
        moves = self.get_ordered_moves(self.game_engine, self.player)
        if len(moves) == 0:
            print "No Valid moves"
            return None
        for x, y in moves:
            self.game_engine.update(x, y)
            flips = cp.deepcopy(self.game_engine.get_last_flips())
            result = -self.alpha_beta(1-self.game_engine.get_currentplayer(), self.depth, bestresult, self.infinite)
            # self.game_engine.display(force=True)
            # print result
            # raw_input()
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
            flips = cp.deepcopy(self.game_engine.get_last_flips())
            result = -self.alpha_beta(player, depth - 1, -beta, -alpha)
            self.game_engine.undo_move(x, y, flips)
            if result >= beta:
                return beta
            if result > alpha:
                alpha = result
        return alpha


if __name__ == '__main__':
    cmd = raw_input("Start a new Game (y/n)? : ")
    bot = AI_bot(show = True, depth = 0)
    while cmd == "y" or cmd == "Y":
        bot.restart()
        cmd = raw_input("You want black(1)/white(0)? (default is black): ")
        if cmd == "1" or cmd.lower() == "black":
            bot.set_player(0)
        else:
            bot.set_player(1)
        while not bot.get_engine().finished():
            if bot.get_engine().get_currentplayer(number = True) != bot.get_player():
                print "Your turn:", bot.get_engine().get_currentplayer(number = False)
                cmd = raw_input("input x, y: ")
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
        cmd = raw_input("Start a new Game (y/n)? : ")
