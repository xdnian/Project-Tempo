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
from paip_othello_class import othello as Paip

c_PUCT = 5

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
        return self.Q + self.U

    def is_expanded(self):
        return self.paip is not None

    def compute_paip(self):
        self.paip = self.parent.paip.deepcopy
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
        self.Q, self.U = (
            self.Q + (value - self.Q) / self.N,
            c_PUCT * math.sqrt(self.parent.N) * self.prior / self.N,
        )
        # must invert, because alternate layers have opposite desires
        self.parent.backup_value(-value)

    def select_leaf(self):
        current = self
        while current.is_expanded():
            current = max(current.children.values(), key=lambda node: node.action_score)
        return current


class MCTS(object):
    def __init__(self, policy_network, seconds_per_move=5):
        self.policy_network = policy_network
        self.seconds_per_move = seconds_per_move
        self.max_rollout_depth = 3
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
            self.tree_search(root)
        # there's a theoretical bug here: if you refuse to pass, this AI will
        # eventually start filling in its own eyes.
        return max(root.children.keys(), key=lambda move, root=root: root.children[move].N)

    def tree_search(self, root):
        print("tree search")
        # selection
        chosen_leaf = root.select_leaf()
        # expansion
        paip = chosen_leaf.compute_paip()
        if paip is None:
            print("illegal move!")
            # See go.paip.play_move for notes on detecting legality
            del chosen_leaf.parent.children[chosen_leaf.move]
            return
        print("Investigating following paip:\n%s" % (chosen_leaf.paip,))
        move_probs = self.policy_network.evaluate(paip)
        chosen_leaf.expand(move_probs)
        # evaluation
        value = self.estimate_value(chosen_leaf)
        # backup
        print("value: %s" % value)
        chosen_leaf.backup_value(value)

    def estimate_value(self, chosen_leaf):
        # Estimate value of paip using rollout only (for now).
        # (TODO: Value network; average the value estimations from rollout + value network)
        leaf_paip = chosen_leaf.paip
        current = leaf_paip
        i = 0
        while i < self.max_rollout_depth:
            if current.player == None:
                break
            move_probs = self.policy_network.evaluate(current)
            current = self.play_valid_move(current, move_probs)
            i+=1
            # In othello, we do not let the player to pass, thus there will be no move called None
            # if len(current.recent) > 2 and current.recent[-1].move == current.recent[-2].move == None:
            #     break
        else:
            print("max rollout depth exceeded!")

        perspective = 1 if leaf_paip.currentplayer else -1
        # should be current score evaluated by the value network
        return current.value * perspective

    def play_valid_move(self, paip, move_probs):
        for move in sorted_moves(move_probs):
            # There is no eyeish in othello
            # if go.is_eyeish(paip.board, move):
            #     continue
            candidate_pos = paip.make_valid_move(move)
            if candidate_pos is not None:
                return candidate_pos
        # return paip.pass_move(mutate=True)
        # print "ERROR!"
