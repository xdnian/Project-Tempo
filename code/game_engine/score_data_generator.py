from othello import othello_engine as oe
import numpy as np
import os

class generator(object):
    """
    This class intend to generate the data for training from the existing file
    """

    def __init__(self, dirname):
        self.dirname = dirname
        self.oe = oe()

    def get_generate_data(self):
        print "start"
        files = os.listdir(self.dirname)
        length = 0
        for filename in files:
            length += sum(1 for line in open(self.dirname + "/" + filename, "r"))
        data = np.empty((length,5,8,8),dtype="int8")
        label = np.empty((length),dtype="float32")
        print length
        data_id = 0
        for filename in files:
            with open(self.dirname + "/" + filename, "r") as f:
                self.oe.restart()
                for line in f:
                    currentplayer = int(line[0])
                    x = int(line[2])
                    y = int(line[4])
                    score = float(line[6:])
                    if self.oe.get_currentplayer() == currentplayer:
                        if not self.oe.update(x, y):
                            print("Fatal error")
                            return
                        eval_player = self.oe.get_currentplayer()
                        gameboard = self.oe.get_board()
                        validboards = self.oe.get_validboard(return_all=True)
                        arr = np.empty((5,8,8), dtype="int8")
                        for i in range(8):
                            for j in range(8):
                                if gameboard[i][j] == eval_player:
                                    arr[0][i][j] = 1
                                    arr[1][i][j] = 1
                                    arr[2][i][j] = 0
                                elif gameboard[i][j] == 1 - eval_player:
                                    arr[0][i][j] = -1
                                    arr[1][i][j] = 0
                                    arr[2][i][j] = 1
                                else:
                                    arr[0][i][j] = 0
                                    arr[1][i][j] = 0
                                    arr[2][i][j] = 0
                                if validboards[currentplayer][i][j] == eval_player:
                                    arr[3][i][j] = 1
                                else:
                                    arr[3][i][j] = 0
                                if validboards[1-currentplayer][i][j] == 1-eval_player:
                                    arr[4][i][j] = 1
                                else:
                                    arr[4][i][j] = 0
                        data[data_id,:,:,:] = arr
                        label[data_id] = -score
                    else:
                        print currentplayer, self.oe.get_currentplayer()
                        print("Fatal error")
                        return
                    data_id += 1

        print "Over!"
        return data, label
