import time
import paip_othello_class as paip
# import cnn_evaluate as CNN
import cnn_evaluate_10 as CNN

matches = 100
report_cycle = 10
min_search_depth = 2
max_search_depth = 3
battle_with_WSS = True
battle_with_random = True

OPTIONS = {
    'random': paip.random_strategy,
    # 'max-diff': paip.maximizer(paip.othello.score),
    # 'max-weighted-diff': paip.maximizer(paip.weighted_score),
    # 'minimax-diff': paip.minimax_searcher(depth, paip.othello.score),
    # 'minimax-weighted-diff':
    #     paip.minimax_searcher(depth, paip.weighted_score),
    # 'ab-diff': paip.alphabeta_searcher(depth, paip.othello.score),
    'ab-weighted-diff':
        paip.alphabeta_searcher(depth, paip.weighted_score),
    'ab-cnn': paip.alphabeta_searcher(depth, CNN.CNN_strategy)
    }

class battle_bot(object):
    '''
    This class is for the battle between AIs. The first heuristic is for the white, the second is for the black.
    '''
    def __init__(self, depth=2, infinite=1000, heuristic=[]):
        self.depth = depth
        self.infinite = infinite

        if heuristic == []:
            self.heuristic = [OPTIONS['ab-weighted-diff']] * 2
        else:
            self.heuristic = [OPTIONS[heuristic[0]], OPTIONS[heuristic[1]]]

    def loop(self, iterations, count):
        k = 0
        sum_black = 0
        sum_white = 0
        draw = 0
        game = paip.othello()
        for i in xrange(iterations):
            if k >= count:
                k = 0
                print "Black wins:", sum_black, "/", i, ", winning rate =", sum_black*1.0/i
                print "White wins:", sum_white, "/", i, ", winning rate =", sum_white*1.0/i
                print "Draw:", draw, "/", i, "draw rate =", draw*1.0/i
                
            _, score = game.play(self.heuristic[0], self.heuristic[1])

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

def match_set(model, opponent, model_side, depth=1):
    if model_side == "black":
        black = model
        white = opponent
    elif model_side == "white":
        black = opponent
        white = model
    print "Black:", black, "v.s. White:", white
    Start = time.time()
    battle = battle_bot(depth=depth, heuristic=[black, white])
    battle.loop(matches, report_cycle)
    End = time.time()
    print "Time:", round(End-Start,3), "Average match Time:", round(End-Start,3)*1.0/matches
    print

if __name__=='__main__':

    CNN.load("./model/CNN_cat_model_L_500.h5")
    # CNN.load("./model/CNN_cat_10_model_L_1000.h5")
    # CNN.load("./model/CNN_cat_model_L_conv4x4sigx64_conv3x3sigx128_fulltanh512_fulltanh128_5000.h5")
    model = 'ab-cnn'

    for depth in range(min_search_depth, max_search_depth):
        print "\n\n==> Search depth: ", depth
        if battle_with_WSS:
            match_set(model, 'ab-weighted-diff', "black", depth)
            match_set(model, 'ab-weighted-diff', "white", depth)
        if battle_with_random:
            match_set(model, 'random', "black", depth)
            match_set(model, 'random', "white", depth)
