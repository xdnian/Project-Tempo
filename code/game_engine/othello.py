from os import system as sys
from platform import system as system
from datetime import datetime as date
import copy as cp

class othello_engine(object):
    """
    The class is the the othello engine
    If you want to initialize the engine with an existed engine, set the parent= GameEngineFrom
    If you want to record the replay, set record = True
    If you want to see the showing of gameboard, set show = True
    """
    def __init__(self, parent = None, show = False, record = False):
        self.pieces = ['x', 'o'] #pieces color
        self.show = show
        self.record = record
        if (self.record):
            with open("Othello_Record.txt", "a+") as f:
                time = date.now()
                f.write("\n" + "--- "+ time.date + "-" + time.month + "-" + time.day + " " + time.hour + ":" + time.minute + ":" + time.second+ " ---\n")
                f.close()
        if (parent == None):
            self.gameboard = []  # gameboard
            self.currentplayer = 0
            self.stones = [0, 0] #stone number for each player
            self.validmoves = [0, 0] # possible moves for each player
            self.validboard = [[], []] # the possible moves's board for each player
            self.end = False
            self.count = 0
            self.replay = ""
            self.restart()
        else:
            self.gameboard = cp.deepcopy(parent.get_board())  # gameboard
            self.currentplayer = cp.deepcopy(parent.get_currentplayer, number = True)
            self.stones = cp.deepcopy(parent.get_stones(), return_all = True) #stone number for each player
            self.validmoves = cp.deepcopy(parent.get_validmoves(), return_all = True) # possible moves for each player
            self.validboard = cp.deepcopy(parent.get_validboard(), return_all = True) # the possible moves's board for each player
            self.end = cp.deepcopy(parent.finished())
            self.count = cp.deepcopy(parent.get_count())
            self.replay = cp.deepcopy(parent.get_replay())

    def get_board(self):
        return self.gameboard

    def get_stones(self, player = None, return_all = False):
        if (return_all):
            return self.stones
        return self.stones[self.currentplayer]

    def get_validboard(self, player = None, return_all = False):
        if (return_all):
            return self.validboard
        return self.validboard[self.currentplayer]

    def get_validmoves(self, player = None, return_all = False):
        if (return_all):
            return self.validmoves
        return self.validmoves[self.currentplayer]

    def get_currentplayer(self, number = False):
        if (number):
            return self.currentplayer
        else:
            return self.pieces[self.currentplayer]
    def get_count(self):
        return self.count

    def get_replay(self):
        return self.replay



    def set_show(self, show):
        self.show = show

    def set_record(self, record):
        self.record = record


    def print_replay(self):
        print self.count, self.replay

    def finished(self):
        return self.end


    def __display(self, force = False):
        if(force or self.show):
            if (system() == 'Windows'):
                sys("cls")
            else:
                sys("clear")
            print "  0 1 2 3 4 5 6 7"
            for i in range(8):
                print str(i) + " " + ' '.join(self.gameboard[i])
            print

    def __record(self):
        if (self.record):
            with open("Othello_Record.txt", "a+") as f:
                f.write(str(self.count) + ": " + self.replay + "\n")
                f.close()

    # prepare the new board for the new game
    def restart(self):
        self.count += 1;
        self.replay  = ""
        self.end = False
        self.currentplayer = 0
        if len(self.gameboard) == 0:
            for i in range(8):
                self.gameboard.append(list("________"))
                self.validboard[0].append(list("________"))
                self.validboard[1].append(list("________"))
        else:
            for i in range(8):
                self.gameboard[i] =list("________")
                self.validboard[0][i] = list("________")
                self.validboard[1][i] = list("________")
        self.gameboard[3][3] = self.pieces[1]
        self.gameboard[3][4] = self.pieces[0]
        self.gameboard[4][3] = self.pieces[0]
        self.gameboard[4][4] = self.pieces[1]
        self.__validateAndCount()
        self.__display()

    # Change the self.pieces in certain directions between target point and end point.
    # The @current_piece is the current color the target point, or assumed color of it during idnetifying whether the point will a valid move.
    # The @change is a boolean. True if it is a actual move, False if it is an assumed move.
    def __change_inside(self, target_x, target_y, end_x, end_y, current_piece, change):
        i = target_x
        j = target_y
        listx = []
        listy = []
        num = 0
        found = False
        while (not found and (i != end_x or j != end_y)):
            if (end_x - i != 0):
                i = i + (end_x - i)/abs(end_x - i)
            if (end_y - j != 0):
                j = j + (end_y - j)/abs(end_y - j)
            if (self.gameboard[i][j] == '_'):
                return False
            elif (self.gameboard[i][j] == current_piece):
                found = True
                break
            listx.append(i)
            listy.append(j)
            num = num + 1
        if (num == 0 or not found):
            return False
        elif (change == True):
            for n in range(num):
                self.gameboard[listx[n]][listy[n]] = current_piece
        return True

    # Expand from the target point in 8 directions.
    # The @current_piece is the current color the target point, or assumed color of it during idnetifying whether the point will a valid move.
    # The @change is a boolean. True if it is a actual move, False if it is an assumed move.
    def __expand(self, target_x, target_y, current_piece, change):
        enable = False
        up = min(target_x, target_y)
        down = min(7 - target_x, 7 - target_y)
        left = min(target_x, 7 - target_y)
        right = min(7 - target_x, target_y)

        if (self.__change_inside(target_x, target_y, 0, target_y, current_piece, change)):
            enable = True
        if (self.__change_inside(target_x, target_y, 7, target_y, current_piece, change)):
            enable = True
        if (self.__change_inside(target_x, target_y, target_x, 0, current_piece, change)):
            enable = True
        if (self.__change_inside(target_x, target_y, target_x, 7, current_piece, change)):
            enable = True
        if (self.__change_inside(target_x, target_y, target_x-up, target_y-up, current_piece, change)):
            enable = True
        if (self.__change_inside(target_x, target_y, target_x-left, target_y+left, current_piece, change)):
            enable = True
        if (self.__change_inside(target_x, target_y, target_x+down, target_y+down, current_piece, change)):
            enable = True
        if (self.__change_inside(target_x, target_y, target_x+right, target_y-right, current_piece, change)):
            enable = True

        if (enable == True):
            return True
        else:
            return False

    # mark the valid possible moves on the xboard and oboard
    def __validateAndCount(self):
        self.stones[0] = 0
        self.stones[1] = 0
        self.validmoves[0] = 0
        self.validmoves[1] = 0
        for i in range(8):
            for j in range(8):
                for k in range(2):
                    self.validboard[k][i][j] = '_'
                    if (self.gameboard[i][j] == '_'):
                        if (self.__expand(i, j, self.pieces[k], False)):
                            self.validboard[k][i][j] = self.pieces[k]
                            self.validmoves[k]+= 1
                    elif (self.gameboard[i][j] == self.pieces[k]):
                        self.stones[k] += 1

    def update(self, x, y):
        if (self.end == True):
            return
        if (self.validboard[self.currentplayer][x][y] != self.pieces[self.currentplayer]):
            self.__display(force = True)
            print "Invalid move!:", x, y
            return
        self.gameboard[x][y] = self.pieces[self.currentplayer]
        self.replay = self.replay + " " + str(self.currentplayer) + str(x) + str(y)
        #update the self.gameboard
        self.__expand(x, y, self.pieces[self.currentplayer], True)
        #update the self.validboard and self.validmoves
        self.__validateAndCount()
        if (self.validmoves[1 - self.currentplayer] != 0):
            self.currentplayer = 1 - self.currentplayer
        if(self.stones[0] == 0 or self.stones[1] == 0 or self.stones[0]+self.stones[1] == 64 or (self.validmoves[0]== 0 and self.validmoves[1] == 0)):
            self.end = True
            self.__record()
            self.__display()
            if (self.stones[0] > self.stones[1]):
                self.replay = "Black" + self.replay
                return "Black"
            elif (self.stones[0] < self.stones[1]):
                self.replay = "White" + self.replay
                return "White"
            else:
                self.replay = "Draw" + self.replay
                return "Draw"
        self.__display()

    def process_file(self, filename):
        fout = open(filename+"_replay", "w")
        with open(filename, "r") as f:
            for line in f:
                self.restart()
                output = ""
                moves = line.split()
                for move in moves:
                    self.update(ord(move[1]) - ord('1'), ord(move[0]) - ord('A'))
                fout.write(self.replay+"\n")
            f.close()
        fout.close()

if  __name__ == '__main__':
    cmd = raw_input("Start a new Game (y/n)? :")
    engine = othello_engine(show = True)
    while (cmd == "y" or cmd == "Y"):
        while (not engine.finished()):
            print "currentplayer is ", engine.get_currentplayer()
            cmd = raw_input("input x, y: ")
            if (len(cmd) > 2):
                if (cmd[0].isdigit() and cmd[2].isdigit()):
                    engine.update(ord(cmd[0]) - ord('0'), ord(cmd[2]) - ord('0'))
        cmd = raw_input("Start a new Game (y/n)? :")
