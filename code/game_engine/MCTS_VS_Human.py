import MCTS

from policyNetwork import PolicyNetwork
from randomNetwork import RandomNetwork
from valueNetwork import ValueNetwork

from utils import *

def check(move, player, board):
    return Othello.is_valid(move) and Othello.is_legal(move, player, board)

def human(player, board):
    print("Note: 'x' denotes black disks, 'o' denotes white disks.")
    print("After computer's response, the board becomes:")
    print Othello.print_board(board)
    while True:
        pos = [int(i) for i in raw_input('your move in "x y"> ').split()]
        if len(pos) == 2:
            move = pos[0] + pos[1]*10 + 11
            if move and check(int(move), player, board):
                return int(move)
            elif move:
                print 'Illegal move--try again.'
        else:
            print 'Illegal input--try again.'

if __name__=='__main__':
    model_human = human
    model_MCTS_random = MCTS.MCTS(prior_prob=RandomNetwork(), seconds_per_move=5, rollout_policy=RandomNetwork())
    model_MCTS_policy = MCTS.MCTS(
                                  prior_prob=PolicyNetwork("./model/policy_model_L_conv5*128_conv3*128*4_20.h5"),
                                  rollout_policy=PolicyNetwork("./model/policy_model_L_conv5*128_conv3*128*4_20.h5"),
                                  seconds_per_move=5
                                 )
    MCTS.play_with_MCTS (Othello(), model_human, model_MCTS_random)
