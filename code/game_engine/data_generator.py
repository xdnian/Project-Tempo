from othello import othello_engine as oe
import numpy as np

class generator(object):
    """
    This class intend to generate the data for training from the existing file
    """

    def __init__(self, filename):
        self.filename = filename
        self.oe = oe()

    def get_generate_data(self):
        print "start"
        length = 0
        data = []
        label = []
        data_id = 0
        with open(self.filename, "r") as f:
            length = sum(len(line.split()) for line in f)
            raw_data = np.empty((length, 6, 8, 8), dtype="int8")
        print length
        with open(self.filename, "r") as f:
            for line in f:
                self.oe.restart()
                moves = line.split()
                for move in moves:
                    currentplayer = ord(move[0]) - ord('0')
                    x = ord(move[1]) - ord('0')
                    y = ord(move[2]) - ord('0')
                    if self.oe.get_currentplayer() == currentplayer:
                        gameboard = self.oe.get_board()
                        validboards = self.oe.get_validboard(return_all=True)
                        arr = np.empty((6, 8, 8), dtype="int8")
                        for i in range(8):
                            for j in range(8):
                                if gameboard[i][j] == currentplayer:
                                    arr[0][i][j] = 1
                                    arr[1][i][j] = 1
                                    arr[2][i][j] = 0
                                elif gameboard[i][j] == 1 - currentplayer:
                                    arr[0][i][j] = -1
                                    arr[1][i][j] = 0
                                    arr[2][i][j] = 1
                                else:
                                    arr[0][i][j] = 0
                                    arr[1][i][j] = 0
                                    arr[2][i][j] = 0
                                if validboards[currentplayer][i][j] == currentplayer:
                                    arr[3][i][j] = 1
                                else:
                                    arr[3][i][j] = 0
                                if validboards[1-currentplayer][i][j] == 1-currentplayer:
                                    arr[4][i][j] = 1
                                else:
                                    arr[4][i][j] = 0
                                if i*8+j <= x*8+y:
                                    arr[5][i][j] = 1
                                else:
                                    arr[5][i][j] = 0
                        raw_data[data_id, :, :, :] = arr
                    else:
                        print currentplayer, self.oe.get_currentplayer()
                        print("Fatal error")
                        return
                    if not self.oe.update(x, y):
                        print("Fatal error")
                        return
                    data_id += 1
        print "Over!"
        np.random.shuffle(raw_data)
        data = np.array(raw_data[:,0:5,:,:])
        label = np.reshape(raw_data[:,5,:,:], (length, 64))
        label = np.asarray(list(sum(i)-1 for i in label))
        return data, label
