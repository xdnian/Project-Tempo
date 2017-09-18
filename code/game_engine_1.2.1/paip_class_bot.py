import paip_othello_class as paip
import time

def check(move, player, board):
    return paip.othello.is_valid(move) and paip.othello.is_legal(move, player, board)

def human(player, board):
    print paip.othello.print_board(board)
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
                CNN.load("./model/CNN_cat_model_L_500.h5")
                return paip.alphabeta_searcher(3, CNN.CNN_strategy)
            return options[choice]
        elif choice:
            print 'Invalid choice.'

def get_players():
    print 'Welcome to OTHELLO!'
    options = { 'human': human,
                'random': paip.random_strategy,
                'max-diff': paip.maximizer(paip.othello.score),
                'max-weighted-diff': paip.maximizer(paip.weighted_score),
                'minimax-diff': paip.minimax_searcher(3, paip.othello.score),
                'minimax-weighted-diff':
                    paip.minimax_searcher(3, paip.weighted_score),
                'ab-diff': paip.alphabeta_searcher(3, paip.othello.score),
                'ab-weighted-diff':
                    paip.alphabeta_searcher(3, paip.weighted_score),
                'ab-cnn': None}
    black = get_choice('BLACK: choose a strategy', options)
    white = get_choice('WHITE: choose a strategy', options)
    
    return black, white
#
def main():
    try:
        black, white = get_players()
        start_time = time.time()
        game = paip.othello()
        board, score = game.play(black, white)
    except paip.IllegalMoveError as e:
        print e
        return
    except EOFError as e:
        print 'Goodbye.'
        return
    print 'Final score:', score
    print '%s wins!' % ('Black' if score > 0 else 'White')
    print paip.othello.print_board(board)

    end_time = time.time()
    print 'Total time = ', end_time-start_time

if  __name__ == '__main__':
    main()
    