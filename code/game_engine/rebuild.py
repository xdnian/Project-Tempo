'''
rebuild mcts tree from sb result!!!!!!!!!
'''
import os
import sys
import time
import math
from utils import *

DATA_DIR = "./mcts_results/origin/"
DEST_DIR = "./mcts_results/policy/"

board_list = [  ['$$$$$$$$$$$........$$........$$........$$...xo...$$...xo...$$...xo...$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$........$$..ooo...$$...xx...$$...x....$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$........$$...xo...$$...ox...$$..ox....$$........$$........$$$$$$$$$$$'],

                ['$$$$$$$$$$$........$$........$$....x...$$...xx...$$...ooo..$$........$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$...ox...$$...ox...$$...ox...$$........$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$....xo..$$...xo...$$...ox...$$........$$........$$........$$$$$$$$$$$'],


                ['$$$$$$$$$$$........$$........$$........$$...xo...$$..xxo...$$....o...$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$........$$..ooo...$$..xxx...$$........$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$........$$...xo...$$..xox...$$..o.....$$........$$........$$$$$$$$$$$'],

                ['$$$$$$$$$$$........$$........$$........$$...xxx..$$...ooo..$$........$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$...o....$$...oxx..$$...ox...$$........$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$.....o..$$...xox..$$...ox...$$........$$........$$........$$$$$$$$$$$']
            ]

parent_list = [ '$$$$$$$$$$$........$$........$$........$$...xo...$$...xx...$$...x....$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$....x...$$...xx...$$...ox...$$........$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$........$$...xo...$$..xxx...$$........$$........$$........$$$$$$$$$$$',
                '$$$$$$$$$$$........$$........$$........$$...xxx..$$...ox...$$........$$........$$........$$$$$$$$$$$']


# Exploration constant
class MCTSNode(object):
    @staticmethod
    def root_node(game):
        node = MCTSNode(None, None)
        node.game = game
        node.expand()
        return node

    def __init__(self, parent, move):
        self.parent = parent # pointer to another MCTSNode
        self.move = move # the move that led to this node
        self.is_played = False
        self.game = None # lazily computed upon expansion
        self.children = {} # map of moves to resulting MCTSNode
        self.Q = 0
        self.N = 0


    def __repr__(self):
        return "<MCTSNode move=%s>" % (self.move)

    def compute_game(self):
        self.game = self.parent.game.deepcopy
        self.game.make_valid_move(self.move)
        return self.game

    def expand(self):
        moves = Othello.legal_moves(self.game.player, self.game.board)
        self.children = {move: MCTSNode(self, move) for move in moves}
        for i in self.children:
            self.children[i].compute_game()


class MCTS(object):
    def __init__(self):
        self.root = None
        self.open = []

    def clear(self):
        self.root = None

    def build_root(self, board):
        if self.root is None:
            if board in parent_list:
                self.root = MCTSNode.root_node(Othello())
                self.init_open()
                return True
            else:
                for i in xrange(4):
                    if board in board_list[i]:
                        self.root = MCTSNode.root_node(Othello(list(parent_list[i]), WHITE))
                        self.init_open()
                        return True

        print "ERROR! ROOT has been built!"
        raw_input()

    def init_open(self):
        for i in self.root.children:
            self.open.append(self.root.children[i])

    def tree_search(self, board, Q, N):
        while len(self.open) > 0:
            temp_node = self.open.pop(0)
            if temp_node.game.board == list(board):
                temp_node.is_played = True
                temp_node.Q = Q
                temp_node.N = N
                temp_node.expand()
                for i in temp_node.children:
                    self.open.append(temp_node.children[i])
                return True
        return False

    def store_value(self, filename):
        # filename = time.strftime('mcts_result_%Y%m%d%H%M%S.txt')
        try:
            with open(DEST_DIR+filename, 'w') as f:
                expansion_list = []
                for i in self.root.children:
                    if self.root.children[i].is_played:
                        expansion_list.append(self.root.children[i])
                while len(expansion_list) > 0:
                    temp_node = expansion_list.pop(0)
                    if not temp_node.is_played or temp_node.game.player is None:
                        continue
                    for i in temp_node.children:
                        if temp_node.children[i].is_played:
                            expansion_list.append(temp_node.children[i])
                    f.write(Othello.board_to_str(temp_node.game.board, temp_node.game.player)+' '+str(temp_node.Q)+' '+str(temp_node.N)+'\n')
        except Exception as e:
            print str(e)
            print "Error! Cannot log file: " + filename

if __name__ == '__main__':
    files = os.listdir(DATA_DIR)
    length = len(files)
    i = 1
    for filename in files:
        with open(DATA_DIR + filename, 'r') as f:
            root_is_built = False
            mcts = MCTS()
            success = True
            for line in f:
                values = line.split(' ')
                board = values[0]
                Q = float(values[1])
                N = int(values[2])

                if not root_is_built:
                    root_is_built = mcts.build_root(board)

                if not mcts.tree_search(board, Q, N):
                    print("Fail at tree searching on: " + filename)
                    print(Othello.print_board(board))
                    success = not success
                    continue

            if success:
                mcts.store_value(filename)

        # progress report
        percentage = int((float(i+1) / (length)) * 30)
        progress_bar = '[' + '='*percentage + '>' + '.'*(29-percentage) + ']'
        sys.stdout.write(' ' + str(i+1) + '/' + str(length) + ' ' + progress_bar + '\r')
        sys.stdout.flush()

        i+=1
