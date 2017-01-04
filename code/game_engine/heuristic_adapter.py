from simple_ai import ai_bot as Bot
import numpy as np
from keras.models import load_model
from keras.models import Sequential

class Model_bot(Bot):
    '''
    This is a subclass of ai_bot, typically designed for the model_based AI.
    '''
    def __init__(self, show = False, record = False, player = 1, model = None, depth = 2, infinite = 1000):
        super(Model_bot, self).__init__(show, record, player, depth, infinite)
        if model == None:
            self.heuristic = self.simple_heuristic
        else:
            self.heuristic = self.model_heuristic
            self.model = load_model(model)

    def model_heuristic(self, engine, player):
        data = np.empty((1,5,8,8), dtype="int8")
        gameboard = self.game_engine.get_board()
        validboards = self.game_engine.get_validboard(return_all=True)
        arr = np.empty((5,8,8), dtype="int8")
        for i in range(8):
            for j in range(8):
                if gameboard[i][j] == 1-player:
                    arr[0][i][j] = 1
                    arr[1][i][j] = 1
                    arr[2][i][j] = 0
                elif gameboard[i][j] == player:
                    arr[0][i][j] = -1
                    arr[1][i][j] = 0
                    arr[2][i][j] = 1
                else:
                    arr[0][i][j] = 0
                    arr[1][i][j] = 0
                    arr[2][i][j] = 0
                if validboards[1-player][i][j] == 1-player:
                    arr[3][i][j] = 1
                else:
                    arr[3][i][j] = 0
                if validboards[player][i][j] == player:
                    arr[4][i][j] = 1
                else:
                    arr[4][i][j] = 0
        data[0,:,:,:] = arr
        score = self.model.predict(data, batch_size=1)
        return score
