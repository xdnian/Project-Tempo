"""
**Othello** is a turn-based two-player strategy board game.  The players take
turns placing pieces--one player white and the other player black--on an 8x8
board in such a way that captures some of the opponent's pieces, with the goal
of finishing the game with more pieces of their color on the board.

Every move must capture one more more of the opponent's pieces.  To capture,
player A places a piece adjacent to one of player B's pieces so that there is a
straight line (horizontal, vertical, or diagonal) of adjacent pieces that begins
with one of player A's pieces, continues with one more more of player B's
pieces, and ends with one of player A's pieces.

For example, if Black places a piece on square (5, 3), he will capture all of
Black's pieces between (5, 3) and (3, 3):


    7 . . . . . . . .    7 . . . . . . . .
    6 . . . . . . . .    6 . . . . . . . .
    5 . . . . . . . .    5 . . . . . . . .
    4 . . . o x . . .    4 . . . o x . . .
    3 . . . x o . . .    3 . . . x x x . .
    2 . . . . . . . .    2 . . . . . . . .
    1 . . . . . . . .    1 . . . . . . . .
    0 . . . . . . . .    0 . . . . . . . .
      0 1 2 3 4 5 6 7      0 1 2 3 4 5 6 7

For more more information about the game (which is also known as Reversi)
including detailed rules, see the entry on [Wikipedia][wiki].  Additionally,
this implementation doesn't take into account some tournament-style Othello
details, such as game time limits and a different indexing scheme.

We will implement representations for the board and pieces and the mechanics of
playing a game.  We will then explore several game-playing strategies.  There is
a simple command-line program [provided](examples/othello/othello.html) for
playing against the computer or comparing two strategies.

Written by [Daniel Connelly](http://dhconnelly.com).  This implementation follows
chapter 18 of Peter Norvig's "Paradigms of Artificial Intelligence".

[wiki]: http://en.wikipedia.org/wiki/Reversi

"""


# -----------------------------------------------------------------------------
## Board representation

# We represent the board as a 100-element list, which includes each square on
# the board as well as the outside edge.  Each consecutive sublist of ten
# elements represents a single row, and each list element stores a piece.  An
# initial board contains four pieces in the center:

#     $ $ $ $ $ $ $ $ $ $
#     $ . . . . . . . . $
#     $ . . . . . . . . $
#     $ . . . . . . . . $
#     $ . . . o x . . . $
#     $ . . . x o . . . $
#     $ . . . . . . . . $
#     $ . . . . . . . . $
#     $ . . . . . . . . $
#     $ $ $ $ $ $ $ $ $ $

# This representation has two useful properties:
#
# 1. Square (m,n) can be accessed as `board[mn]`.  This avoids the need to write
#    functions that convert between square locations and list indexes.
# 2. Operations involving bounds checking are slightly simpler.

# The outside edge is marked $, empty squares are ., black is x, and white is o.
# The black and white pieces represent the two players.
WHITE, BLACK, EMPTY, OUTER = 'o', 'x', '.', '$'
PIECES = (WHITE, BLACK, EMPTY, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = 10, -10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = 11, -9, -11, 9
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
DIRECTIONS4 = (UP, RIGHT, DOWN, LEFT)

class othello():
    def __init__(self, board=None, player=BLACK):
        if board is not None:
            self.__board = board
        else:
            self.__board = self.initial_board()
        self.__player = player

    @property
    def board(self):
        return self.__board

    @property
    def player(self):
        return self.__player

    @property
    def currentplayer(self):
        return self.__player == BLACK

    @property
    def deepcopy(self):
        return othello(list(self.__board), self.__player)

    @staticmethod
    def squares():
        """List all the valid squares on the board."""
        return [i for i in xrange(11, 89) if 1 <= (i % 10) <= 8]

    @staticmethod
    def initial_board():
        """Create a new board with the initial black and white positions filled."""
        board = [OUTER] * 100
        for i in othello.squares():
            board[i] = EMPTY
        # The middle four squares should hold the initial piece positions.
        board[44], board[45] = WHITE, BLACK
        board[54], board[55] = BLACK, WHITE
        return board

    @staticmethod
    def print_board(board):
        """Get a string representation of the board."""
        rep = ''
        for row in xrange(8, 0, -1):
            begin, end = 10*row + 1, 10*row + 9
            rep += '%d %s\n' % (row-1, ' '.join(board[begin:end]))
        rep += '  %s\n' % ' '.join(map(str, range(8)))
        return rep


    # -----------------------------------------------------------------------------
    ## Playing the game

    # We need functions to get moves from players, check to make sure that the moves
    # are legal, apply the moves to the board, and detect when the game is over.

    ### Checking moves

    # A move must be both valid and legal: it must refer to a real square, and it
    # must form a bracket with another piece of the same color with pieces of the
    # opposite color in between.

    @staticmethod
    def is_valid(move):
        """Is move a square on the board?"""
        return isinstance(move, int) and move in othello.squares()

    @staticmethod
    def opponent(player):
        """Get player's opponent piece."""
        return BLACK if player is WHITE else WHITE

    @staticmethod
    def find_bracket(square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        """
        bracket = square + direction
        if board[bracket] == player:
            return None
        opp = othello.opponent(player)
        while board[bracket] == opp:
            bracket += direction
        return None if board[bracket] in (OUTER, EMPTY) else bracket

    @staticmethod
    def is_legal(move, player, board):
        """Is this a legal move for the player?"""
        hasbracket = lambda direction: othello.find_bracket(move, player, board, direction)
        return board[move] == EMPTY and any(map(hasbracket, DIRECTIONS))

    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    @staticmethod
    def make_move(move, player, board):
        """Update the board to reflect the move by the specified player."""
        board[move] = player
        for d in DIRECTIONS:
            othello.make_flips(move, player, board, d)
        return board

    def make_valid_move(self, move):
        if not othello.is_valid(move) or not othello.is_legal(move, self.__player, self.__board):
            print othello.print_board(self.__board)
            print self.__player
            raise IllegalMoveError(self.__player, move, self.__board)
        else:
            if self.__player is not None:
                othello.make_move(move, self.__player, self.__board)
                self.__player = othello.next_player(self.__board, self.__player)

    @staticmethod
    def make_flips(move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        bracket = othello.find_bracket(move, player, board, direction)
        if not bracket:
            return
        square = move + direction
        while square != bracket:
            board[square] = player
            square += direction

    ### Monitoring players
    @staticmethod
    def legal_moves(player, board):
        """Get a list of all legal moves for player."""
        return [sq for sq in othello.squares() if othello.is_legal(sq, player, board)]

    @staticmethod
    def any_legal_move(player, board):
        """Can player make any moves?"""
        return any(othello.is_legal(sq, player, board) for sq in othello.squares())

    ### Putting it all together

    # Each round consists of:
    #
    # - Get a move from the current player.
    # - Apply it to the board.
    # - Switch players.  If the game is over, get the final score.

    def restart(self):
        self.__board = othello.initial_board()
        self.__player = BLACK

    def play(self, black_strategy, white_strategy):
        """Play a game of Othello and return the final board and score."""
        self.restart()
        strategy = lambda who: black_strategy if who == BLACK else white_strategy
        while self.__player is not None:
            move = othello.get_move(strategy(self.__player), self.__player, self.__board)
            othello.make_move(move, self.__player, self.__board)
            self.__player = othello.next_player(self.__board, self.__player)
        return self.__board, othello.score(BLACK, self.__board)

    def play_with_MCTS(self, MCTS, other_strategy, MCTSisBlack):
        # self.restart()
        while self.__player is not None:
            if self.currentplayer == MCTSisBlack:
                move = MCTS.suggest_move(self)
                othello.make_move(move, self.__player, self.__board)
            else:
                move = othello.get_move(other_strategy, self.__player, self.__board)
                othello.make_move(move, self.__player, self.__board)
            print move
            print othello.print_board(self.__board)
            self.__player = othello.next_player(self.__board, self.__player)
            # raw_input()
        return self.__board, othello.score(BLACK, self.__board)


    @staticmethod
    def next_player(board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        opp = othello.opponent(prev_player)
        if othello.any_legal_move(opp, board):
            return opp
        elif othello.any_legal_move(prev_player, board):
            return prev_player
        return None

    @staticmethod
    def get_move(strategy, player, board):
        """Call strategy(player, board) to get a move."""
        copy = list(board) # copy the board to prevent cheating
        move = strategy(player, copy)
        if not othello.is_valid(move) or not othello.is_legal(move, player, board):
            raise IllegalMoveError(player, move, copy)
        return move

    @staticmethod
    def score(player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        mine, theirs = 0, 0
        opp = othello.opponent(player)
        for sq in othello.squares():
            piece = board[sq]
            if piece == player: mine += 1
            elif piece == opp: theirs += 1
        return mine - theirs

    @property
    def value(self):
        """Compute player's score (number of player's pieces minus opponent's)."""
        black, white = 0, 0
        for sq in othello.squares():
            piece = self.__board[sq]
            if piece == BLACK: black += 1
            elif piece == WHITE: white += 1
        if black == white:
            return 0.5
        elif black > white:
            return 1
        else:
            return 0

class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)


# -----------------------------------------------------------------------------
## Play strategies

### Random

import random

def random_strategy(player, board):
    """A strategy that always chooses a random legal move."""
    return random.choice(othello.legal_moves(player, board))

### Local maximization

def maximizer(evaluate):
    """
    Construct a strategy that chooses the best move by maximizing
    evaluate(player, board) over all boards resulting from legal moves.
    """
    def strategy(player, board):
        def score_move(move):
            return evaluate(player, othello.make_move(move, player, list(board)))
        return max(othello.legal_moves(player, board), key=score_move)
    return strategy


SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]

# SQUARE_WEIGHTS = [
#     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
#     0,10.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5,10.5,   0,
#     0, 5.5,   1,   1,   1,   1,   1,   1, 5.5,   0,
#     0, 5.5,   1,   1,   1,   1,   1,   1, 5.5,   0,
#     0, 5.5,   1,   1,   1,   1,   1,   1, 5.5,   0,
#     0, 5.5,   1,   1,   1,   1,   1,   1, 5.5,   0,
#     0, 5.5,   1,   1,   1,   1,   1,   1, 5.5,   0,
#     0, 5.5,   1,   1,   1,   1,   1,   1, 5.5,   0,
#     0,10.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5,10.5,   0,
#     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
# ]


# A strategy constructed as `maximizer(weighted_score)`, then, will always
# return the move that results in the largest immediate *weighted* gain in
# pieces.

def weighted_score(player, board):
    """
    Compute the difference between the sum of the weights of player's
    squares and the sum of the weights of opponent's squares.
    """
    opp = othello.opponent(player)
    total = 0
    for sq in othello.squares():
        if board[sq] == player:
            total += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTS[sq]
    return total

### Minimax search

def minimax(player, board, depth, evaluate):
    """
    Find the best legal move for player, searching to the specified depth.
    Returns a tuple (move, min_score), where min_score is the guaranteed minimum
    score achievable for player if the move is made.
    """

    # We define the value of a board to be the opposite of its value to our
    # opponent, computed by recursively applying `minimax` for our opponent.
    def value(board):
        return -minimax(othello.opponent(player), board, depth-1, evaluate)[0]

    # When depth is zero, don't examine possible moves--just determine the value
    # of this board to the player.
    if depth == 0:
        return evaluate(player, board), None

    # We want to evaluate all the legal moves by considering their implications
    # `depth` turns in advance.  First, find all the legal moves.
    moves = othello.legal_moves(player, board)

    # If player has no legal moves, then either:
    if not moves:
        # the game is over, so the best achievable score is victory or defeat;
        if not othello.any_legal_move(othello.opponent(player), board):
            return final_value(player, board), None
        # or we have to pass this turn, so just find the value of this board.
        return value(board), None

    # When there are multiple legal moves available, choose the best one by
    # maximizing the value of the resulting boards.
    random.shuffle(moves)
    return max((value(othello.make_move(m, player, list(board))), m) for m in moves)

# Values for endgame boards are big constants.
MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

def final_value(player, board):
    """The game is over--find the value of this board to player."""
    diff = othello.score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff

def minimax_searcher(depth, evaluate):
    """
    Construct a strategy that uses `minimax` with the specified leaf board
    evaluation function.
    """
    def strategy(player, board):
        return minimax(player, board, depth, evaluate)[1]
    return strategy

### Alpha-Beta search

def alphabeta(player, board, alpha, beta, depth, evaluate):
    """
    Find the best legal move for player, searching to the specified depth.  Like
    minimax, but uses the bounds alpha and beta to prune branches.
    """
    if depth == 0:
        return evaluate(player, board), None

    def value(board, alpha, beta):
        # Like in `minimax`, the value of a board is the opposite of its value
        # to the opponent.  We pass in `-beta` and `-alpha` as the alpha and
        # beta values, respectively, for the opponent, since `alpha` represents
        # the best score we know we can achieve and is therefore the worst score
        # achievable by the opponent.  Similarly, `beta` is the worst score that
        # our opponent can hold us to, so it is the best score that they can
        # achieve.
        return -alphabeta(othello.opponent(player), board, -beta, -alpha, depth-1, evaluate)[0]

    moves = othello.legal_moves(player, board)
    if not moves:
        if not othello.any_legal_move(othello.opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None

    random.shuffle(moves)
    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            # If one of the legal moves leads to a better score than beta, then
            # the opponent will avoid this branch, so we can quit looking.
            break
        val = value(othello.make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
            # If one of the moves leads to a better score than the current best
            # achievable score, then replace it with this one.
            alpha = val
            best_move = move
    return alpha, best_move

def alphabeta_searcher(depth, evaluate):
    def strategy(player, board):
        return alphabeta(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate)[1]
    return strategy

#-------------------------------------------------------------------------------
#-------------------------------Split line for MCTS-----------------------------
#-------------------------------------------------------------------------------

"""
Rewrite notes for the MCTS:
1. paip is the go engine, it should be replaced by the othello engine
2. Some of the functions should refer to the original *.py file
3. Policy network and value network should be replaced as ours
4. Calling the policy network with evaluate() should return a list of pair [(move, probabilities)]
5. Calling the paip with make_move(move, mutate = True/False) should make move
6. Calling the paip with score() currently should return the difference of stones
"""

from keras.models import Sequential, load_model
from policyNetwork import PolicyNetwork
import time
import math

c_PUCT = 0.05

def sorted_moves(probability_array):
    return list(probability_array[i][0] for i in sorted(range(len(probability_array)), key=lambda c: probability_array[c][1], reverse=True))

# Exploration constant
class MCTSNode(object):
    '''
    A MCTSNode has two states: plain, and expanded.
    An plain MCTSNode merely knows its Q + U values, so that a decision
    can be made about which MCTS node to expand during the selection phase.
    When expanded, a MCTSNode also knows the actual paip at that node,
    as well as followup moves/probabilities via the policy network.
    Each of these followup moves is instantiated as a plain MCTSNode.
    '''
    @staticmethod
    def root_node(paip, move_probabilities):
        node = MCTSNode(None, None, 0)
        node.paip = paip
        node.expand(move_probabilities)
        return node

    def __init__(self, parent, move, prior):
        self.parent = parent # pointer to another MCTSNode
        self.move = move # the move that led to this node
        self.prior = prior
        self.paip = None # lazily computed upon expansion
        self.children = {} # map of moves to resulting MCTSNode
        self.Q = self.parent.Q if self.parent is not None else 0 # average of all outcomes involving this node
        self.U = prior # monte carlo exploration bonus
        self.N = 0 # number of times node was visited

    def __repr__(self):
        return "<MCTSNode move=%s prior=%s score=%s is_expanded=%s>" % (self.move, self.prior, self.action_score, self.is_expanded())

    @property
    def action_score(self):
        # Note to self: after adding value network, must calculate
        # self.Q = weighted_average(avg(values), avg(rollouts)),
        # as opposed to avg(map(weighted_average, values, rollouts))
        if self.N == 0:
            self.U = 1.5 + c_PUCT * self.prior
        else:
            self.U = c_PUCT * math.sqrt(self.prior) * self.parent.N / self.N
        return self.Q + self.U

    def is_expanded(self):
        return self.paip is not None

    def compute_paip(self):
        self.paip = self.parent.paip.deepcopy
        # DEBUG
        # if self.move == 64:
        #     print othello.print_board(self.paip.board)
        #     print othello.legal_moves(self.paip.player, self.paip.board)
        #     node = self
        #     while node.parent != None:
        #         print node.move
        #         print othello.print_board(node.parent.paip.board)
        #         print othello.legal_moves(node.parent.paip.player, node.parent.paip.board)
        #         print
        #         node = node.parent
        self.paip.make_valid_move(self.move)
        return self.paip

    def expand(self, move_probabilities):
        self.children = {move: MCTSNode(self, move, prob)
            for move, prob in move_probabilities}
        ## Pass should always be an option! Say, for example, seki.
        # There should be no move called pass for othello
        # self.children[None] = MCTSNode(self, None, 0)

    def backup_value(self, value):
        self.N += 1
        if self.parent is None:
            # No point in updating Q / U values for root, since they are
            # used to decide between children nodes.
            return
        self.Q = self.Q + (math.floor(value) - self.Q) / self.N
        # must invert, because alternate layers have opposite desires\
        if self.paip.player == None:
            self.parent.backup_value(value if self.parent.paip.currentplayer else 1-value)
            # print value if self.parent.paip.currentplayer else 1-value
        else:
            self.parent.backup_value(value if self.parent.paip.player == self.paip.player else 1-value)
            # print value if self.parent.paip.player == self.paip.player else 1-value


    def select_leaf(self):
        current = self
        while current.is_expanded():
            if len(current.children) == 0:
                return None
            current = max(current.children.values(), key=lambda node: node.action_score)
        return current


class MCTS(object):
    def __init__(self, policy_network, seconds_per_move=5):
        self.policy_network = policy_network
        self.seconds_per_move = seconds_per_move
        self.max_rollout_depth = 60
        # self.model = model

    def clear(self):
        self.refresh_network()

    # def refresh_network(self):
    #     # Ensure that the player is using the latest version of the network
    #     # so that the network can be continually trained even as it's playing.
    #     self.policy_network.load_model(self.model)

    def suggest_move(self, paip):
        # We do not want our othello AI to resign! Fight to the end!
        # if paip.caps[0] + 50 < paip.caps[1]:
        #     return gtp.RESIGN
        start = time.time()
        move_probs = self.policy_network.evaluate(paip)
        root = MCTSNode.root_node(paip, move_probs)
        while time.time() - start < self.seconds_per_move:
            if not self.tree_search(root):
                break
        # there's a theoretical bug here: if you refuse to pass, this AI will
        # eventually start filling in its own eyes.
        for i in root.children.keys():
            print i, root.children[i].Q, root.children[i].action_score, root.children[i].N
        return max(root.children.keys(), key=lambda move, root=root: root.children[move].Q)

    def tree_search(self, root):
        # print("tree search")
        # selection
        chosen_leaf = root.select_leaf()
        if chosen_leaf == None:
            return False
        # expansion
        paip = chosen_leaf.compute_paip()
        if paip is None:
            print("illegal move!")
            # See go.paip.play_move for notes on detecting legality
            del chosen_leaf.parent.children[chosen_leaf.move]
            return
        # print("Investigating following paip:\n%s" % (chosen_leaf.paip,))
        move_probs = self.policy_network.evaluate(paip)
        # DEBUG
        # print move_probs
        # print paip.player
        # print othello.print_board(paip.board)
        # print othello.legal_moves(paip.player,paip.board)
        # print
        chosen_leaf.expand(move_probs)
        # evaluation
        value = self.estimate_value(chosen_leaf)
        # backup
        # print("value: %s" % value)
        chosen_leaf.backup_value(value)
        return True

    def estimate_value(self, chosen_leaf):
        # Estimate value of paip using rollout only (for now).
        # (TODO: Value network; average the value estimations from rollout + value network)
        leaf_paip = chosen_leaf.paip
        current = leaf_paip.deepcopy
        i = 0
        while i < self.max_rollout_depth and current.player is not None:
            move_probs = self.policy_network.evaluate(current)
            current = self.play_valid_move(current, move_probs)
            i+=1
            # In othello, we do not let the player to pass, thus there will be no move called None
            # if len(current.recent) > 2 and current.recent[-1].move == current.recent[-2].move == None:
            #     break
        else:
            pass
            # print("max rollout depth exceeded!")

        score = current.value
        if chosen_leaf.parent == None:
            print "ERROR"
            return None
        score = score if chosen_leaf.parent.paip.currentplayer else 1 - score
        # should be current score evaluated by the value network
        return score

    def play_valid_move(self, paip, move_probs):
        # DEBUG
        if len(move_probs) == 0:
            print othello.print_board(paip.board)
            print paip.player
            raw_input()
        paip.make_valid_move(sorted_moves(move_probs)[0])
        return paip
        # for move in sorted_moves(move_probs):
        #     # There is no eyeish in othello
        #     # if go.is_eyeish(paip.board, move):
        #     #     continue
        #     candidate_pos = paip.make_valid_move(move)
        #     if candidate_pos is not None:
        #         return candidate_pos
        # return paip.pass_move(mutate=True)
        # print "ERROR!"
