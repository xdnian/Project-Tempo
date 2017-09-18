import numpy as np
from keras.models import load_model
from keras.models import Sequential

class heuristic(object):
    def evaluate(self, engine, player):
        print "Warning! This method is supposed to be overwritten!"
        return 0

    def check_adjacent(self, i, j, board):
        for n in [-1,1]:
            if i+n < 8 and i+n > -1:
                if board[i+n][j] == -1:
                    return True
            if j+n < 8 and j+n > -1:
                if board[i][j+n] == -1:
                    return True
        return False

class random_heuristic(heuristic):
    def evaluate(self, engine, player):
        return 0

    def __str__(self):
        return "Random"

class simple_heuristic(heuristic):
    '''
    first value is the corner, the second is the side
    '''
    def __init__(self, points = [10.5, 5.5]):
        self.points = points

    def set_points(self, points):
        self.points = points

    def evaluate(self, engine, player):
        board = engine.get_board()
        value = 0
        for x, y in [(0,0),(0,7),(7,0),(7,7)]:
            if board[x][y] == player:
                value += self.points[0]
            elif board[x][y] == 1-player:
                value -= self.points[0]
        for x in [0,7]:
            for y in range(8)[1:-1]:
                if board[x][y] == player:
                    value += self.points[1]
                elif board[x][y] == 1-player:
                    value -= self.points[1]
                if board[y][x] == player:
                    value += self.points[1]
                elif board[y][x] == 1-player:
                    value -= self.points[1]
        for x in range(8)[1:-1]:
            for y in range(8)[1:-1]:
                if board[x][y] == player:
                    value += 1
                elif board[x][y] == 1-player:
                    value -= 1
        ###DEBUG
        # print value
        # raw_input()
        ###DEBUG
        return value

    def __str__(self):
        return "Weighted Square Strategy"

class CNN_heuristic(heuristic):
    def __init__(self, model):
        self.model = load_model(model)

    def set_model(self, model):
        self.model = load_model(model)

    def evaluate(self, engine, player):
        data = np.empty((1,9,8,8), dtype="int8")
        gameboard = engine.get_board()
        validboards = engine.get_validboard(return_all=True)
        arr = np.empty((9,8,8), dtype="int8")
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
                if gameboard[i][j] == -1:
                    arr[5][i][j] = 0
                    arr[6][i][j] = 0
                    arr[7][i][j] = 0
                    arr[8][i][j] = 0
                elif self.check_adjacent(i, j, gameboard):
                    if gameboard[i][j] == player:
                        arr[5][i][j] = 1
                        arr[6][i][j] = 0
                        arr[7][i][j] = 0
                        arr[8][i][j] = 0
                    elif gameboard[i][j] == 1-player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 0
                        arr[7][i][j] = 1
                        arr[8][i][j] = 0
                else:
                    if gameboard[i][j] == player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 1
                        arr[7][i][j] = 0
                        arr[8][i][j] = 0
                    elif gameboard[i][j] == 1-player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 0
                        arr[7][i][j] = 0
                        arr[8][i][j] = 1
        data[0,:,:,:] = arr
        value = self.model.predict(data, batch_size=1)
        # ##DEBUG
        # print value
        # raw_input()
        # ##DEBUG
        return -value

    def __str__(self):
        return "CNN_Score"

class MLP_heuristic(heuristic):
    def __init__(self, model):
        self.model = load_model(model)

    def set_model(self, model):
        self.model = load_model(model)

    def evaluate(self, engine, player):
        data = np.empty((1,9,8,8), dtype="int8")
        gameboard = engine.get_board()
        validboards = engine.get_validboard(return_all=True)
        arr = np.empty((9,8,8), dtype="int8")
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
                if gameboard[i][j] == -1:
                    arr[5][i][j] = 0
                    arr[6][i][j] = 0
                    arr[7][i][j] = 0
                    arr[8][i][j] = 0
                elif self.check_adjacent(i, j, gameboard):
                    if gameboard[i][j] == player:
                        arr[5][i][j] = 1
                        arr[6][i][j] = 0
                        arr[7][i][j] = 0
                        arr[8][i][j] = 0
                    elif gameboard[i][j] == 1-player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 0
                        arr[7][i][j] = 1
                        arr[8][i][j] = 0
                else:
                    if gameboard[i][j] == player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 1
                        arr[7][i][j] = 0
                        arr[8][i][j] = 0
                    elif gameboard[i][j] == 1-player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 0
                        arr[7][i][j] = 0
                        arr[8][i][j] = 1
        data[0,:,:,:] = arr
        data = data.reshape(data.shape[0], data.shape[1]*data.shape[2]*data.shape[3])
        value = self.model.predict(data, batch_size=1)
        ###DEBUG
        # print value
        # raw_input()
        ###DEBUG
        return -value

    def __str__(self):
        return "MLP_Score"

class MLP_CAT_heuristic(heuristic):
    def __init__(self, model):
        self.model = load_model(model)

    def set_model(self, model):
        self.model = load_model(model)

    def evaluate(self, engine, player):
        data = np.empty((1,11,8,8), dtype="int8")
        gameboard = engine.get_board()
        validboards = engine.get_validboard(return_all=True)
        arr = np.empty((11,8,8), dtype="int8")
        for i in range(8):
            for j in range(8):
                arr[0][i][j] = 0
                if i==0 or i==7 or j==0 or j==7:
                    arr[9][i][j] = 100
                else:
                    arr[9][i][j] = 0
                arr[10][i][j] = 100
                if gameboard[i][j] == 1:
                    arr[1][i][j] = 100
                    arr[2][i][j] = 100
                    arr[3][i][j] = 0
                elif gameboard[i][j] == 0:
                    arr[1][i][j] = 100
                    arr[2][i][j] = 0
                    arr[3][i][j] = 100
                else:
                    arr[1][i][j] = 0
                    arr[2][i][j] = 0
                    arr[3][i][j] = 0
                if validboards[player][i][j] == player:
                    arr[4][i][j] = 100
                else:
                    arr[4][i][j] = 0
                if gameboard[i][j] == -1:
                    arr[5][i][j] = 0
                    arr[6][i][j] = 0
                    arr[7][i][j] = 0
                    arr[8][i][j] = 0
                elif self.check_adjacent(i, j, gameboard):
                    if gameboard[i][j] == 1:
                        arr[5][i][j] = 100
                        arr[6][i][j] = 0
                        arr[7][i][j] = 0
                        arr[8][i][j] = 0
                    elif gameboard[i][j] == 0:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 0
                        arr[7][i][j] = 100
                        arr[8][i][j] = 0
                else:
                    if gameboard[i][j] == 1:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 100
                        arr[7][i][j] = 0
                        arr[8][i][j] = 0
                    elif gameboard[i][j] == 0:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 0
                        arr[7][i][j] = 0
                        arr[8][i][j] = 100
        data[0,:,:,:] = arr
        data = data.reshape(data.shape[0], data.shape[1]*data.shape[2]*data.shape[3])
        cat = self.model.predict(data, batch_size=1)
        value = np.argmax(cat[0])-20
        ##DEBUG
        print value
        raw_input()
        ##DEBUG
        return value if player == 1 else -value

    def __str__(self):
        return "MLP_CAT"

class CNN_CAT_heuristic(heuristic):
    def __init__(self, model):
        self.model = load_model(model)

    def set_model(self, model):
        self.model = load_model(model)

    def evaluate(self, engine, player):
        data = np.empty((1,11,8,8), dtype="int8")
        gameboard = engine.get_board()
        validboards = engine.get_validboard(return_all=True)
        arr = np.empty((11,8,8), dtype="int8")
        for i in range(8):
            for j in range(8):
                arr[0][i][j] = 0
                if i==0 or i==7 or j==0 or j==7:
                    arr[9][i][j] = 1
                else:
                    arr[9][i][j] = 0
                arr[10][i][j] = 1
                if gameboard[i][j] == player:
                    arr[1][i][j] = 1
                    arr[2][i][j] = 0
                    arr[3][i][j] = 0
                elif gameboard[i][j] == 1-player:
                    arr[1][i][j] = 0
                    arr[2][i][j] = 1
                    arr[3][i][j] = 0
                else:
                    arr[1][i][j] = 0
                    arr[2][i][j] = 0
                    arr[3][i][j] = 1
                if validboards[player][i][j] == player:
                    arr[4][i][j] = 1
                else:
                    arr[4][i][j] = 0
                if gameboard[i][j] == -1:
                    arr[5][i][j] = 0
                    arr[6][i][j] = 0
                    arr[7][i][j] = 0
                    arr[8][i][j] = 0
                elif self.check_adjacent(i, j, gameboard):
                    if gameboard[i][j] == player:
                        arr[5][i][j] = 1
                        arr[6][i][j] = 0
                        arr[7][i][j] = 0
                        arr[8][i][j] = 0
                    elif gameboard[i][j] == 1-player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 0
                        arr[7][i][j] = 1
                        arr[8][i][j] = 0
                else:
                    if gameboard[i][j] == player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 1
                        arr[7][i][j] = 0
                        arr[8][i][j] = 0
                    elif gameboard[i][j] == 1-player:
                        arr[5][i][j] = 0
                        arr[6][i][j] = 0
                        arr[7][i][j] = 0
                        arr[8][i][j] = 1
        data[0,:,:,:] = arr
        # engine.display(force=True)
        # print arr
        # raw_input()
        cat = self.model.predict(data, batch_size=1)
        value = np.argmax(cat[0])
        if value > 8:
            value = value - 17
        #DEBUG
        # print value
        # raw_input()
        #DEBUG
        return -value #if player == 1 else -value

    def __str__(self):
        return "CNN_CAT"
