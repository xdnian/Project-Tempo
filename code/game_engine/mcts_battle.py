import time

import utils
from utils import Othello
from MCTS import MCTS as MCTSSearcher
from MCTS import play_with_MCTS

from policyNetwork import PolicyNetwork
from randomNetwork import RandomNetwork
from valueNetwork import ValueNetwork

# init_board=[
#     '$', '$', '$', '$', '$', '$', '$', '$', '$', '$',
#     '$', '.', '.', 'o', 'o', 'o', 'o', '.', '.', '$',
#     '$', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '.', '$',
#     '$', 'o', '.', 'o', '.', 'o', 'o', 'o', 'o', '$',
#     '$', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '.', '$',
#     '$', 'o', 'o', 'o', '.', 'o', 'o', 'o', 'o', '$',
#     '$', 'o', 'o', '.', 'o', '.', 'o', 'o', 'o', '$',
#     '$', 'o', 'o', '.', 'o', 'o', '.', 'o', 'o', '$',
#     '$', 'o', 'o', '.', '.', '.', '.', '.', '.', '$',
#     '$', '$', '$', '$', '$', '$', '$', '$', '$', '$']
# othello = Othello(board=init_board)
# moves = Othello.legal_moves(BLACK, othello.board)
# print moves
# moves = Othello.legal_moves(WHITE, othello.board)
# print moves
# moves = Othello.legal_moves(None, othello.board)
# print moves
# raw_input()



matches = 50
report_cycle = 10
SEARCH_TIME = 5

class battle_bot(object):
    '''
    This class is for the battle between AIs. The first heuristic is for the white, the second is for the black.
    '''
    def __init__(self, heuristic):
        self.heuristic = heuristic
        self.engine = Othello()

    def loop(self, iterations, count):
        k = 0
        sum_black = 0
        sum_white = 0
        draw = 0
        for i in xrange(iterations):
            if k >= count:
                k = 0
                print "Black wins:", sum_black, "/", i, ", winning rate =", sum_black*1.0/i
                print "White wins:", sum_white, "/", i, ", winning rate =", sum_white*1.0/i
                print "Draw:", draw, "/", i, "draw rate =", draw*1.0/i

            _, score = play_with_MCTS(self.engine, self.heuristic[0], self.heuristic[1])
            for i in (0,1):
                if isinstance(self.heuristic[i], MCTSSearcher):
                    self.heuristic[i].clear()

            if score > 0: # black wins
                sum_black += 1
            elif score < 0: # white wins
                sum_white += 1
            elif score == 0: # draw
                draw += 1
            k+=1

        print "Black wins:", sum_black, "/", iterations, ", winning rate =", sum_black*1.0/iterations
        print "White wins:", sum_white, "/", iterations, ", winning rate =", sum_white*1.0/iterations
        print "Draw:", draw, "/", iterations, "draw rate =", draw*1.0/iterations

def match_set(model, opponent, model_side):
    if model_side == "black":
        black = model
        white = opponent
    elif model_side == "white":
        black = opponent
        white = model
    Start = time.time()
    battle = battle_bot(heuristic=[black, white])
    battle.loop(matches, report_cycle)
    End = time.time()
    print "Time:", round(End-Start,3), "Average match Time:", round(End-Start,3)*1.0/matches
    print

if __name__=='__main__':

    depth = 3

    policynetworks = {
        'fast': PolicyNetwork(
            "./model/policy_model_L_conv5*128_conv3*128*4_20.h5"),
            }

    valuenetworks = {
        # 'policy': ValueNetwork('./model/value_model_L_epochs_201704130137.h5'),
        'None': None,
    }

    rollout_dic = {
        # 'use_policy': True,
        'use_random': False,
    }

    use_depth_dic = {
        # 'use_depth': True,
        'no_depth': False,
    }

    opponents = {
        # 'WSS': utils.alphabeta_searcher(depth, utils.weighted_score),
        'mcts_RAN': MCTSSearcher(prior_prob=RandomNetwork(), seconds_per_move=SEARCH_TIME, rollout_policy=RandomNetwork()),
        # 'real_RAN': utils.random_strategy,
    }

    for oppo in opponents:
        for policy_network in policynetworks:
            for value_network in valuenetworks:
                for rollout_policy in policynetworks:
                    for use_depth in use_depth_dic:
                        if value_network == 'None' and use_depth == 'use_depth':
                            continue
                        model_1 = MCTSSearcher(
                                    prior_prob=policynetworks[policy_network],
                                    value_network=valuenetworks[value_network],
                                    rollout_policy=policynetworks[rollout_policy],
                                    use_depth=use_depth,
                                    seconds_per_move=SEARCH_TIME)
                        model_2 = opponents[oppo]

                        # print "Black:", policy_network+"+"+value_network+"+"+rollout_policy+"+"+use_depth, "v.s. White:", oppo
                        # match_set(model_1, model_2, "black")

                        print "Black:", oppo, "v.s. White:", policy_network+"+"+value_network+"+"+rollout_policy+"+"+use_depth
                        match_set(model_1, model_2, "white")

    # model_1 = opponents['WSS']
    # model_2 = opponents['RAN']
    # print "Black: WSS v.s. White: RAN"
    # match_set(model_1, model_2, "black")
    # print "Black: RAN v.s. White: WSS"
    # match_set(model_1, model_2, "white")

    # model_1 = opponents['real-RAN']
    # model_2 = opponents['RAN']
    # print "Black: real-RAN v.s. White: RAN"
    # match_set(model_1, model_2, "black")
    # print "Black: RAN v.s. White: real-RAN"
    # match_set(model_1, model_2, "white")
