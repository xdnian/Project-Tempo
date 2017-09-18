import paip_othello as othello
import time

DEPTH = 1

def check(move, player, board):
    return othello.is_valid(move) and othello.is_legal(move, player, board)

def human(player, board):
    print othello.print_board(board)
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

def get_choice(prompt, options):
    print prompt
    print 'Options:', options.keys()
    while True:
        choice = raw_input('> ')
        if choice in options:
            if choice == 'ab-cnn':
                import cnn_evaluate as CNN
                CNN.load("./model/CNN_cat_model_L_201704161615.h5")
                # CNN.load("./model/CNN_cat_model_L_500.h5")
                return othello.alphabeta_searcher(DEPTH, CNN.CNN_strategy)
            return options[choice]
        elif choice:
            print 'Invalid choice.'

def get_players():
    print 'Welcome to OTHELLO!'
    options = { 'human': human,
                'random': othello.random_strategy,
                'max-diff': othello.maximizer(othello.score),
                'max-weighted-diff': othello.maximizer(othello.weighted_score),
                'minimax-diff': othello.minimax_searcher(DEPTH, othello.score),
                'minimax-weighted-diff':
                    othello.minimax_searcher(DEPTH, othello.weighted_score),
                'ab-diff': othello.alphabeta_searcher(DEPTH, othello.score),
                'ab-weighted-diff':
                    othello.alphabeta_searcher(DEPTH, othello.weighted_score),
                'ab-cnn': None}
    black = get_choice('BLACK: choose a strategy', options)
    white = get_choice('WHITE: choose a strategy', options)

    return black, white
#
def main():
    try:
        black, white = get_players()
        start_time = time.time()
        board, score = othello.play(black, white)
    except othello.IllegalMoveError as e:
        print e
        return
    except EOFError as e:
        print 'Goodbye.'
        return
    print 'Final score:', score
    print '%s wins!' % ('Black' if score > 0 else 'White')
    print othello.print_board(board)

    end_time = time.time()
    print 'Total time = ', end_time-start_time

if  __name__ == '__main__':
    main()
