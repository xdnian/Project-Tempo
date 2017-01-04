from othello import othello_engine as oe
import numpy as np
from keras.models import load_model
from keras.models import Sequential

class ai_bot(object):
    """
    This AI bot is a scretch for a simple AI based on the move prediction.
    """
    def __init__(self, show = False, record = False, player = 1):
        if player == 1 or player.lower() == "black":
            self.player = 1
        else:
            self.player = 0
        self.game_engine = oe(show = show, record = record)
        self.model = load_model('CNN_model.h5')

    def get_engine(self):
        return self.game_engine

    def get_player(self):
        return self.player

    def set_player(self, player):
        if player == 1:
            self.player = 1
        else:
            self.player = 0

    def run_best_move(self):
        self.game_engine.set_show(False)
        (x, y) = self.get_best_move()
        self.game_engine.set_show(True)
        self.game_engine.update(x, y)
        return (x, y)

    def get_best_move(self):
        if self.game_engine.get_validmoves(player=1-self.player) == 0:
            print "No Valid moves"
            return None
        data = np.empty((1,5,8,8), dtype="int8")
        if self.game_engine.get_currentplayer() == 1-self.player:
            gameboard = self.game_engine.get_board()
            validboards = self.game_engine.get_validboard(return_all=True)
            arr = np.empty((5,8,8), dtype="int8")
            for i in range(8):
                for j in range(8):
                    if gameboard[i][j] == 1-self.player:
                        arr[0][i][j] = 1
                        arr[1][i][j] = 1
                        arr[2][i][j] = 0
                    elif gameboard[i][j] == self.player:
                        arr[0][i][j] = -1
                        arr[1][i][j] = 0
                        arr[2][i][j] = 1
                    else:
                        arr[0][i][j] = 0
                        arr[1][i][j] = 0
                        arr[2][i][j] = 0
                    if validboards[1-self.player][i][j] == 1-self.player:
                        arr[3][i][j] = 1
                    else:
                        arr[3][i][j] = 0
                    if validboards[self.player][i][j] == self.player:
                        arr[4][i][j] = 1
                    else:
                        arr[4][i][j] = 0
            data[0,:,:,:] = arr
        else:
            print self.player, self.game_engine.get_currentplayer()
            print("Fatal error")
            return
        x=0
        y=0
        prob = self.model.predict(data, batch_size=1)
        validboard = self.game_engine.get_validboard(player=1-self.player)
        max_prob=0
        for i in range(8):
            for j in range(8):
                if validboard[i][j] == 1-self.player:
                    if prob[0][i*8+j] > max_prob:
                        x = i
                        y = j
                        max_prob = prob[0][i*8+j]
        return (x, y)



if __name__ == '__main__':
    cmd = raw_input("Start a new Game (y/n)? : ")
    bot = ai_bot(show = True)
    while cmd == "y" or cmd == "Y":
        bot.get_engine().restart()
        cmd = raw_input("You want black(1)/white(0)? (default is black): ")
        if cmd == "0" or cmd.lower() == "white":
            bot.set_player(0)
        while not bot.get_engine().finished():
            if bot.get_engine().get_currentplayer(number = True) == bot.get_player():
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
        print bot.get_engine().get_stones(player=1),":",bot.get_engine().get_stones(player=0)
        cmd = raw_input("Start a new Game (y/n)? : ")
