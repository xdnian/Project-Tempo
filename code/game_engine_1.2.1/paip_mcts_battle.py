import time
# from paip_othello_class import othello as Paip
# from paip_othello_class import MCTS as MCTSSearcher
# import paip_othello_class as othello

from paip_othello_class_mcts import othello as Paip
from paip_othello_class_mcts import MCTS as MCTSSearcher
import paip_othello_class_mcts as othello

from policyNetwork import PolicyNetwork
from randomNetwork import RandomNetwork

# init_board=[
#     '$', '$', '$', '$', '$', '$', '$', '$', '$', '$',
#     '$', 'x', 'x', 'x', 'x', 'x', 'x', 'o', 'x', '$',
#     '$', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x', '$',
#     '$', 'o', 'o', 'x', 'o', 'o', 'x', 'o', 'o', '$',
#     '$', 'o', 'o', 'o', 'x', 'x', 'x', 'o', 'o', '$',
#     '$', 'o', 'o', 'o', 'x', 'x', 'o', 'x', 'o', '$',
#     '$', 'o', 'o', 'x', 'o', 'o', 'x', 'o', 'o', '$',
#     '$', 'o', 'o', 'x', 'o', 'o', 'o', 'o', 'o', '$',
#     '$', '.', 'o', 'x', 'x', '.', 'o', 'o', 'x', '$',
#     '$', '$', '$', '$', '$', '$', '$', '$', '$', '$']
# paip = Paip(board=init_board)


matches = 100
report_cycle = 10
SEARCH_TIME = 5

class battle_bot(object):
    '''
    This class is for the battle between AIs. The first heuristic is for the white, the second is for the black.
    '''
    def __init__(self, heuristic):
        self.heuristic = heuristic
        self.engine = Paip()

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

            _, score = self.engine.play_with_MCTS(self.heuristic[0], self.heuristic[1])
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

    # policynetworks = {
    #     'fast': PolicyNetwork(
    #         "./model/p_CNN_cat_10_model_L_conv4x4sigx50_conv3x3sigx100_fulltanh200_fulltanh100_500.h5"
    #     ),
    #     'best': PolicyNetwork(
    #         "./model/p_CNN_cat_10_model_L_conv4x4sigx64_conv3x3sigx128_fulltanh256_fulltanh128_500.h5"
    #     ),
    #     'overfit': PolicyNetwork(
    #         "./model/p_CNN_cat_10_model_L_conv4x4sigx64_conv3x3sigx256_fulltanh512_fulltanh128_1000.h5"
    #     )}

    opponents = {
        'WSS': othello.alphabeta_searcher(depth, othello.weighted_score),
        'RAN': MCTSSearcher(RandomNetwork(), seconds_per_move=SEARCH_TIME)
    }

    # for oppo in opponents:
    #     for network in policynetworks:
    #         model_1 = MCTSSearcher(policynetworks[network], seconds_per_move=SEARCH_TIME)
    #         model_2 = opponents[oppo]
    #
    #         print "Black:", network, "v.s. White:", oppo
    #         match_set(model_1, model_2, "black")
    #
    #         print "Black:", oppo, "v.s. White:", network
    #         match_set(model_1, model_2, "white")

    model_1 = opponents['WSS']
    model_2 = opponents['RAN']
    print "Black: WSS v.s. White: RAN"
    match_set(model_1, model_2, "black")
    print "Black: RAN v.s. White: WSS"
    match_set(model_1, model_2, "white")
