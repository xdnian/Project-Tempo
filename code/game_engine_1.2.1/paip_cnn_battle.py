import time
import paip_othello as othello
import cnn_evaluate as CNN1
import cnn_evaluate_10 as CNN2

matches = 100
report_cycle = 10
min_search_depth = 1
max_search_depth = 3
battle_with_WSS = True
battle_with_random = True

class battle_bot(object):
    '''
    This class is for the battle between AIs. The first heuristic is for the white, the second is for the black.
    '''
    def __init__(self, depth=2, infinite=1000, heuristic=[]):
        self.depth = depth
        self.infinite = infinite
        self.options = {
            'random': othello.random_strategy,
            # 'max-diff': othello.maximizer(othello.score),
            # 'max-weighted-diff': othello.maximizer(othello.weighted_score),
            # 'minimax-diff': othello.minimax_searcher(depth, othello.score),
            # 'minimax-weighted-diff':
            #     othello.minimax_searcher(depth, othello.weighted_score),
            # 'ab-diff': othello.alphabeta_searcher(depth, othello.score),
            'ab-weighted-diff':
                othello.alphabeta_searcher(depth, othello.weighted_score),
            'ab-cnn1': othello.alphabeta_searcher(depth, CNN1.CNN_strategy),
            'ab-cnn2': othello.alphabeta_searcher(depth, CNN2.CNN_strategy)
            }

        if heuristic == []:
            self.heuristic = [self.options['ab-weighted-diff']] * 2
        else:
            self.heuristic = [self.options[heuristic[0]], self.options[heuristic[1]]]

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

            _, score = othello.play(self.heuristic[0], self.heuristic[1])

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

    CNN1.load("./model/CNN_cat_model_L_500.h5")
    CNN2.load("./model/CNN_cat_10_model_L_conv4x4sigx64_conv3x3sigx256_fulltanh512_fulltanh128_bach2000_1000.h5")
    # CNN.load("./model/CNN_cat_model_L_conv4x4sigx64_conv3x3sigx128_fulltanh512_fulltanh128_5000.h5")
    model1 = 'ab-cnn1'
    model2 = 'ab-cnn2'
    for depth in range(min_search_depth, max_search_depth):
        print "\n\n==> Search depth: ", depth
        match_set(model1, model2, "black", 1)
        match_set(model1, model2, "white", 1)


    # for depth in range(min_search_depth, max_search_depth):
    #     print "\n\n==> Search depth: ", depth
    #     if battle_with_WSS:
    #         match_set(model, 'ab-weighted-diff', "black", depth)
    #         match_set(model, 'ab-weighted-diff', "white", depth)
    #     if battle_with_random:
    #         match_set(model, 'random', "black", depth)
    #         match_set(model, 'random', "white", depth)
