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
a simple command-line program [provided](examples/othello/Othello.html) for
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

class Othello():
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
        return Othello(list(self.__board), self.__player)

    @staticmethod
    def squares():
        """List all the valid squares on the board."""
        return [i for i in xrange(11, 89) if 1 <= (i % 10) <= 8]

    @staticmethod
    def initial_board():
        """Create a new board with the initial black and white positions filled."""
        board = [OUTER] * 100
        for i in Othello.squares():
            board[i] = EMPTY
        # The middle four squares should hold the initial piece positions.
        board[44], board[45] = BLACK, WHITE
        board[54], board[55] = WHITE, BLACK
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
        return isinstance(move, int) and move in Othello.squares()

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
        opp = Othello.opponent(player)
        while board[bracket] == opp:
            bracket += direction
        return None if board[bracket] in (OUTER, EMPTY) else bracket

    @staticmethod
    def is_legal(move, player, board):
        """Is this a legal move for the player?"""
        hasbracket = lambda direction: Othello.find_bracket(move, player, board, direction)
        return board[move] == EMPTY and any(map(hasbracket, DIRECTIONS))

    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    @staticmethod
    def make_move(move, player, board):
        """Update the board to reflect the move by the specified player."""
        board[move] = player
        for d in DIRECTIONS:
            Othello.make_flips(move, player, board, d)
        return board

    def make_valid_move(self, move):
        if not Othello.is_valid(move) or not Othello.is_legal(move, self.__player, self.__board):
            print Othello.print_board(self.__board)
            print self.__player
            raise IllegalMoveError(self.__player, move, self.__board)
        else:
            if self.__player is not None:
                Othello.make_move(move, self.__player, self.__board)
                self.__player = Othello.next_player(self.__board, self.__player)

    @staticmethod
    def make_flips(move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        bracket = Othello.find_bracket(move, player, board, direction)
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
        return [sq for sq in Othello.squares() if Othello.is_legal(sq, player, board)]

    @staticmethod
    def any_legal_move(player, board):
        """Can player make any moves?"""
        return any(Othello.is_legal(sq, player, board) for sq in Othello.squares())

    ### Putting it all together

    # Each round consists of:
    #
    # - Get a move from the current player.
    # - Apply it to the board.
    # - Switch players.  If the game is over, get the final score.

    def restart(self):
        self.__board = Othello.initial_board()
        self.__player = BLACK

    def play(self, black_strategy, white_strategy):
        """Play a game of Othello and return the final board and score."""
        self.restart()
        strategy = lambda who: black_strategy if who == BLACK else white_strategy
        while self.__player is not None:
            move = Othello.get_move(strategy(self.__player), self.__player, self.__board)
            Othello.make_move(move, self.__player, self.__board)
            self.__player = Othello.next_player(self.__board, self.__player)
        return self.__board, Othello.score(BLACK, self.__board)

    @staticmethod
    def next_player(board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        opp = Othello.opponent(prev_player)
        if Othello.any_legal_move(opp, board):
            return opp
        elif Othello.any_legal_move(prev_player, board):
            return prev_player
        return None

    @staticmethod
    def get_move(strategy, player, board):
        """Call strategy(player, board) to get a move."""
        copy = list(board) # copy the board to prevent cheating
        move = strategy(player, copy)
        if not Othello.is_valid(move) or not Othello.is_legal(move, player, board):
            raise IllegalMoveError(player, move, copy)
        return move

    @staticmethod
    def score(player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        mine, theirs = 0, 0
        opp = Othello.opponent(player)
        for sq in Othello.squares():
            piece = board[sq]
            if piece == player: mine += 1
            elif piece == opp: theirs += 1
        return mine - theirs

    @property
    def value(self):
        """Compute player's score (number of player's pieces minus opponent's)."""
        black, white = 0, 0
        for sq in Othello.squares():
            piece = self.__board[sq]
            if piece == BLACK: black += 1
            elif piece == WHITE: white += 1
        if black == white:
            return 0.5
        elif black > white:
            return 1
        else:
            return 0

    @staticmethod
    def board_to_str(board, player):
        if player != None:
            return ''.join(board)+' '+player
        else:
            return ''.join(board)+' '+'.'

    @staticmethod
    def str_to_board(string):
        return list(string[:-2]), string[-1]

class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
        # print Othello.print_board(self.board)

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)


# -----------------------------------------------------------------------------
## Play strategies

### Random

import random

def random_strategy(player, board):
    """A strategy that always chooses a random legal move."""
    return random.choice(Othello.legal_moves(player, board))

### Local maximization

def maximizer(evaluate):
    """
    Construct a strategy that chooses the best move by maximizing
    evaluate(player, board) over all boards resulting from legal moves.
    """
    def strategy(player, board):
        def score_move(move):
            return evaluate(player, Othello.make_move(move, player, list(board)))
        return max(Othello.legal_moves(player, board), key=score_move)
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
    opp = Othello.opponent(player)
    total = 0
    for sq in Othello.squares():
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
        return -minimax(Othello.opponent(player), board, depth-1, evaluate)[0]

    # When depth is zero, don't examine possible moves--just determine the value
    # of this board to the player.
    if depth == 0:
        return evaluate(player, board), None

    # We want to evaluate all the legal moves by considering their implications
    # `depth` turns in advance.  First, find all the legal moves.
    moves = Othello.legal_moves(player, board)

    # If player has no legal moves, then either:
    if not moves:
        # the game is over, so the best achievable score is victory or defeat;
        if not Othello.any_legal_move(Othello.opponent(player), board):
            return final_value(player, board), None
        # or we have to pass this turn, so just find the value of this board.
        return value(board), None

    # When there are multiple legal moves available, choose the best one by
    # maximizing the value of the resulting boards.
    random.shuffle(moves)
    return max((value(Othello.make_move(m, player, list(board))), m) for m in moves)

# Values for endgame boards are big constants.
MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

def final_value(player, board):
    """The game is over--find the value of this board to player."""
    diff = Othello.score(player, board)
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
        return -alphabeta(Othello.opponent(player), board, -beta, -alpha, depth-1, evaluate)[0]

    moves = Othello.legal_moves(player, board)
    if not moves:
        if not Othello.any_legal_move(Othello.opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None

    random.shuffle(moves)
    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            # If one of the legal moves leads to a better score than beta, then
            # the opponent will avoid this branch, so we can quit looking.
            break
        val = value(Othello.make_move(move, player, list(board)), alpha, beta)
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
