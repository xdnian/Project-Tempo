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
        self.pieces = ['o', 'x', ' '] #pieces color
        self.show = show
        self.record = record
        if self.record:
            with open("Othello_Record.txt", "a+") as f:
                time = date.now()
                f.write("\n" + "--- "+ time.date + "-" + time.month + "-" + time.day + " " + time.hour + ":" + time.minute + ":" + time.second+ " ---\n")
                f.close()
        if parent == None:
            self.gameboard = []  # gameboard
            self.currentplayer = 1 # 1 is for black, 0 is for white
            self.stones = [0, 0] #stone number for each player
            self.validmoves = [0, 0] # possible moves for each player
            self.validboard = [[], []] # the possible moves's board for each player
            self.end = False
            self.count = 0
            self.replay = ""
            self.restart()
            self.winner = None # 0 for black, 1 for white, -1 for draw
            self.last_flips = []
        else:
            self.gameboard = cp.deepcopy(parent.get_board())
            self.currentplayer = cp.deepcopy(parent.get_currentplayer(number = True))
            self.stones = cp.deepcopy(parent.get_stones(return_all = True))
            self.validmoves = cp.deepcopy(parent.get_validmoves(return_all = True))
            self.validboard = cp.deepcopy(parent.get_validboard(return_all = True))
            self.end = cp.deepcopy(parent.finished())
            self.count = cp.deepcopy(parent.get_count())
            self.replay = cp.deepcopy(parent.get_replay())
            self.winner = cp.deepcopy(parent.get_winner())

    def get_board(self):
        return self.gameboard

    def get_last_flips(self):
        return self.last_flips

    def get_stones(self, player = None, return_all = False):
        if return_all:
            return self.stones
        if player == None:
            player = self.currentplayer
        return self.stones[player]

    def get_validboard(self, player = None, return_all = False):
        if return_all:
            return self.validboard
        if player == None:
            player = self.currentplayer
        return self.validboard[player]

    def get_validmoves(self, player = None, return_all = False):
        if return_all:
            return self.validmoves
        if player == None:
            player = self.currentplayer
        return self.validmoves[player]

    def get_currentplayer(self, number = True):
        if number:
            return self.currentplayer
        else:
            return self.pieces[self.currentplayer]

    def get_count(self):
        return self.count

    def get_replay(self):
        return self.replay

    def get_winner(self):
        return self.winner

    def set_show(self, show):
        self.show = show

    def set_record(self, record):
        self.record = record


    def print_replay(self):
        print self.count, self.replay

    def finished(self):
        return self.end

    # def display(self, force = False, board = None):
    #     if board == None:
    #         board = self.validboard[self.currentplayer]
    #     if force or self.show:
    #         if system() == 'Windows':
    #             sys("cls")
    #         else:
    #             sys("clear")
    #         for i in xrange(8):
    #             print str(7-i) + " " + ' '.join(self.pieces[j] for j in board[7-i])
    #         print "  0 1 2 3 4 5 6 7"
    #         print
    #         raw_input()

    def __display(self, force = False, board = None):
        if board == None:
            board = self.gameboard
        if force or self.show:
            if system() == 'Windows':
                sys("cls")
            else:
                sys("clear")
            for i in xrange(8):
                print str(7-i),
                for j in xrange(8):
                    print self.pieces[board[j][7-i]],
                print
            print "  0 1 2 3 4 5 6 7"
            print

    def __record(self):
        if self.record:
            with open("Othello_Record.txt", "a+") as f:
                f.write(str(self.count) + ": " + self.replay + "\n")
                f.close()

    # prepare the new board for the new game
    def restart(self):
        self.count += 1;
        self.replay  = ""
        self.end = False
        self.currentplayer = 1
        if len(self.gameboard) == 0:
            for i in xrange(8):
                self.gameboard.append([-1]*8)
                self.validboard[0].append([-1]*8)
                self.validboard[1].append([-1]*8)
        else:
            for i in xrange(8):
                self.gameboard[i] =[-1]*8
                self.validboard[0][i] = [-1]*8
                self.validboard[1][i] = [-1]*8
        self.gameboard[3][3] = 1
        self.gameboard[3][4] = 0
        self.gameboard[4][3] = 0
        self.gameboard[4][4] = 1
        self.__validateAndCount()
        self.__display()


    # This method is to undo one move. You should pass in the pieces been flipped in last turn
    def undo_move(self, x, y, flips):
        if self.gameboard[x][y] == -1:
            print "Undo fail! No piece here!"
            return
        self.currentplayer = self.gameboard[x][y]
        self.gameboard[x][y] = -1
        for i, j in flips:
            self.gameboard[i][j] = 1 - self.gameboard[i][j]
        self.__validateAndCount()
        self.end = False

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
        while not found and (i != end_x or j != end_y):
            if end_x - i != 0:
                i = i + (end_x - i)/abs(end_x - i)
            if end_y - j != 0:
                j = j + (end_y - j)/abs(end_y - j)
            if self.gameboard[i][j] == -1:
                return False
            elif self.gameboard[i][j] == current_piece:
                found = True
                break
            listx.append(i)
            listy.append(j)
            num = num + 1
        if num == 0 or not found:
            return False
        elif change == True:
            for n in xrange(num):
                self.gameboard[listx[n]][listy[n]] = current_piece
                self.last_flips.append((listx[n], listy[n]))
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

        if self.__change_inside(target_x, target_y, 0, target_y, current_piece, change):
            enable = True
        if self.__change_inside(target_x, target_y, 7, target_y, current_piece, change):
            enable = True
        if self.__change_inside(target_x, target_y, target_x, 0, current_piece, change):
            enable = True
        if self.__change_inside(target_x, target_y, target_x, 7, current_piece, change):
            enable = True
        if self.__change_inside(target_x, target_y, target_x-up, target_y-up, current_piece, change):
            enable = True
        if self.__change_inside(target_x, target_y, target_x-left, target_y+left, current_piece, change):
            enable = True
        if self.__change_inside(target_x, target_y, target_x+down, target_y+down, current_piece, change):
            enable = True
        if self.__change_inside(target_x, target_y, target_x+right, target_y-right, current_piece, change):
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
        for i in xrange(8):
            for j in xrange(8):
                for k in xrange(2):
                    self.validboard[k][i][j] = -1
                    if self.gameboard[i][j] == -1:
                        if self.__expand(i, j, k, False):
                            self.validboard[k][i][j] = k
                            self.validmoves[k]+= 1
                    elif self.gameboard[i][j] == k:
                        self.stones[k] += 1

    def update(self, x, y):
        if self.end == True:
            return False
        if self.validboard[self.currentplayer][x][y] != self.currentplayer:
            self.__display(force = True)
            print "Invalid move!:", x, y
            return False
        self.gameboard[x][y] = self.currentplayer
        self.replay = self.replay + " " + str(self.currentplayer) + str(x) + str(y)
        #update the self.gameboard
        self.last_flips = []
        self.__expand(x, y, self.currentplayer, True)
        #update the self.validboard and self.validmoves
        self.__validateAndCount()
        if self.validmoves[1 - self.currentplayer] != 0:
            self.currentplayer = 1 - self.currentplayer
        if self.stones[0] == 0 or self.stones[1] == 0 or sum(self.stones) == 64 or (self.validmoves[0]== 0 and self.validmoves[1] == 0):
            self.end = True
            self.__record()
            self.__display()
            if self.stones[1] > self.stones[0]:
                self.winner = 1
                self.replay = "Black" + self.replay
                return "Black"
            elif self.stones[1] < self.stones[0]:
                self.winner = 0
                self.replay = "White" + self.replay
                return "White"
            else:
                self.winner = -1
                self.replay = "Draw" + self.replay
                return "Draw"
        self.__display()
        return True

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
    cmd = raw_input("Start a new Game (y/n)? : ")
    engine = othello_engine(show = True)
    while cmd == "y" or cmd == "Y":
        engine.restart()
        while not engine.finished():
            print "currentplayer is", engine.get_currentplayer(number=False)
            cmd = raw_input("input x, y: ")
            if len(cmd) > 2:
                if cmd[0].isdigit() and cmd[2].isdigit():
                    engine.update(ord(cmd[0]) - ord('0'), ord(cmd[2]) - ord('0'))
        if engine.get_winner() == 0:
            print "Winner is Black!"
        elif engine.get_winner() == 1:
            print "Winner is White!"
        else:
            print "Draw!"
        cmd = raw_input("Start a new Game (y/n)? : ")
