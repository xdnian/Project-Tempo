"""
Rewrite notes for the MCTS:
1. game is the go engine, it should be replaced by the othello engine
2. Some of the functions should refer to the original *.py file
3. Policy network and value network should be replaced as ours
4. Calling the policy network with evaluate() should return a list of pair [(move, probabilities)]
5. Calling the game with make_move(move, mutate = True/False) should make move
6. Calling the game with score() currently should return the difference of stones
"""
import time
import math
from utils import Othello
import utils
import random

c_PUCT = 5
lamda = 0.5
max_simulations = 500
DEST_DIR = "./mcts_results/random/"
ERROR_DIR = "./mcts_results/error/"

def sorted_moves(probability_array):
    return list(probability_array[i][0] for i in sorted(range(len(probability_array)), key=lambda c: probability_array[c][1], reverse=True))

# Exploration constant
class MCTSNode(object):
    '''
    A MCTSNode has two states: plain, and expanded.
    An plain MCTSNode merely knows its Q + U values, so that a decision
    can be made about which MCTS node to expand during the selection phase.
    When expanded, a MCTSNode also knows the actual game at that node,
    as well as followup moves/probabilities via the policy network.
    Each of these followup moves is instantiated as a plain MCTSNode.
    '''
    @staticmethod
    def root_node(game, move_probabilities):
        node = MCTSNode(None, None, 0)
        node.game = game
        node.expand(move_probabilities)
        return node

    def __init__(self, parent, move, prior):
        self.parent = parent # pointer to another MCTSNode
        self.move = move # the move that led to this node
        self.prior = prior
        self.game = None # lazily computed upon expansion
        self.children = {} # map of moves to resulting MCTSNode
        self.Q = self.parent.Q if self.parent is not None else 0 # average of all outcomes involving this node
        self.U = prior # monte carlo exploration bonus
        self.N = 0 # number of times node was visited

    def __repr__(self):
        return "<MCTSNode move=%s prior=%s score=%s is_expanded=%s>" % (self.move, self.prior, self.action_score, self.is_expanded())

    @property
    def action_score(self):
        if self.N == 0:
            self.U = 1.5 + c_PUCT * self.prior
        else:
            # self.U = c_PUCT * math.sqrt(self.prior) * self.parent.N / self.N
            self.U = 0.5 * math.sqrt(self.prior * self.parent.N) / self.N #for random
        return self.Q + self.U

    def is_expanded(self):
        return self.game is not None

    def compute_game(self):
        self.game = self.parent.game.deepcopy
        self.game.make_valid_move(self.move)
        return self.game

    def expand(self, move_probabilities):
        self.children = {move: MCTSNode(self, move, prob)
            for move, prob in move_probabilities}

    def backup_value(self, value):
        self.N += 1
        if self.parent is None:
            # No point in updating Q / U values for root, since they are
            # used to decide between children nodes.
            return True
        self.Q = self.Q + (value - self.Q) / self.N
        # must invert, because alternate layers have opposite desires\

        if self.game.player == None:
            value = value if self.parent.game.currentplayer else 1-value
            # print value if self.parent.game.currentplayer else 1-value
        else:
            value = value if self.parent.game.player == self.game.player else 1-value
            # print value if self.parent.game.player == self.game.player else 1-value

        try:
            return self.parent.backup_value(value)
        except Exception as e:
            print str(e)
            return False



    def select_leaf(self):
        current = self
        while current.is_expanded():
            if len(current.children) == 0:
                return None
            current = max(current.children.values(), key=lambda node: node.action_score)
        return current


class MCTS(object):
    def __init__(self, prior_prob=None, value_network=None, seconds_per_move=5, rollout_policy=None, use_depth=False, value_only_once = False):
        self.prior_prob = prior_prob
        self.value_network = value_network
        self.seconds_per_move = seconds_per_move
        self.rollout_policy = rollout_policy
        self.root = None
        self.current_root = None
        self.max_rollout_depth = 60
        self.use_depth = use_depth
        self.value_only_once = value_only_once
        self.depth = 1

    def clear(self):
        self.root = None

    def suggest_move(self, game):
        start = time.time()
        if self.root is None:
            move_probs = self.prior_prob.evaluate(game)
            self.root = MCTSNode.root_node(game.deepcopy, move_probs)
            self.current_root = self.root

        simulations = 0
        while time.time() - start < self.seconds_per_move and simulations < max_simulations:
            simulations += 1
            if not self.tree_search(self.current_root):
                break
        self.depth += 1
        # for i in self.current_root.children.keys():
        #     print i, round(self.current_root.children[i].Q, 4),\
        #              round(self.current_root.children[i].U, 4),\
        #              self.current_root.children[i].N
        # raw_input()
        return max(self.current_root.children.keys(), key=lambda move, root=self.current_root: root.children[move].Q)

    def shift_root(self, move):
        if self.root is None:
            return
        if move in self.current_root.children:
            self.current_root = self.current_root.children[move]
            if not self.current_root.is_expanded():
                self.tree_search(self.current_root)
        else:
            print ("\n\n\n\nFatal Error\n\n\n\n")
            # move_probs = self.prior_prob.evaluate(self.current_root.game)
            # self.current_root.expand(move_probs)
            # self.current_root = self.current_root.children[move]

    def tree_search(self, root):
        # print("tree search")
        # selection
        chosen_leaf = root.select_leaf()
        if chosen_leaf == None:
            return False
        # expansion
        game = chosen_leaf.compute_game()
        if game is None:
            print("illegal move!")
            del chosen_leaf.parent.children[chosen_leaf.move]
            return
        if game.player is not None:
            move_probs = self.prior_prob.evaluate(game)
            chosen_leaf.expand(move_probs)
        # evaluation
        value = self.estimate_value(chosen_leaf)
        # backup
        # print("value: %s" % value)
        if not chosen_leaf.backup_value(value):
            self.store_value(ERROR_DIR)
            raw_input()
        return True

    def estimate_value(self, chosen_leaf):
        leaf_game = chosen_leaf.game
        current = leaf_game.deepcopy
        score = 0

        if self.value_only_once and self.value_network is not None and self.depth < 25 and chosen_leaf.N == 0:
                score = self.value_network.evaluate(leaf_game)
        else:
            i = 0
            while i < self.max_rollout_depth and current.player is not None:
                current = self.play_valid_move(current)
                i+=1
            score = current.value

        if chosen_leaf.parent == None:
            print ("ERROR")
            return None
        score = score if chosen_leaf.parent.game.currentplayer else 1 - score
        # weighted mean of rollout and value network score
        if leaf_game.player is not None and self.value_network is not None:
            if self.use_depth:
                score = (self.depth * lamda * score + (30 - self.depth) * (1-lamda) * self.value_network.evaluate(leaf_game)) / (self.depth * lamda + (30 - self.depth) * (1-lamda))
            else:
                score = lamda * score + (1-lamda) * self.value_network.evaluate(leaf_game)
        return score

    def play_valid_move(self, game):
        move_probs = self.rollout_policy.evaluate(game)
        game.make_valid_move(sorted_moves(move_probs)[0])
        return game

    def store_value(self, dest=DEST_DIR):
        filename = time.strftime('mcts_result_%Y%m%d%H%M%S.txt')
        try:
            with open(dest+filename, 'w') as f:
                expansion_list = []
                for i in self.root.children:
                    if self.root.children[i].is_expanded():
                        expansion_list.append(self.root.children[i])
                while len(expansion_list) > 0:
                    temp_node = expansion_list.pop(0)
                    if temp_node.game.player is None:
                        continue
                    for i in temp_node.children:
                        if temp_node.children[i].is_expanded():
                            expansion_list.append(temp_node.children[i])
                    f.write(Othello.board_to_str(temp_node.game.board, temp_node.game.player)+' '+str(temp_node.Q)+' '+str(temp_node.N)+'\n')
        except:
            print "Error! Cannot log file: " + filename

def play_with_MCTS(game, black_strategy, white_strategy):
    game.restart()
    strategy = lambda who: black_strategy if who == utils.BLACK else white_strategy

    while game.player is not None:
        game_strategy = strategy(game.player)
        oppo_strategy = strategy(Othello.opponent(game.player))

        if isinstance(game_strategy, MCTS):
            move = game_strategy.suggest_move(game)
            game_strategy.shift_root(move)
        else:
            move = Othello.get_move(game_strategy, game.player, game.board)

        if isinstance(oppo_strategy, MCTS):
            oppo_strategy.shift_root(move)

        game.make_valid_move(move)
        # print move
        # print Othello.print_board(game.board)
        # game.player = Othello.next_player(game.board, game.player)
        # raw_input()

    # Store the value for value network training
    # if isinstance(black_strategy, MCTS):
    #     black_strategy.store_value()
    # if isinstance(white_strategy, MCTS):
    #     white_strategy.store_value()

    return game.board, Othello.score(utils.BLACK, game.board)
