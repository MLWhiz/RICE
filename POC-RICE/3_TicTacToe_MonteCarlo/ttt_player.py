"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 70       # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """This function takes a current board and the next player to move. The function should play a game starting with the given player by making 
random moves, alternating between players. The function should return when the game is over. The modified board will contain the state of the game, 
so the function does not return anything. In other words, the function should modify the board input."""
    winner = board.check_win()
    while winner is None:
        player_move = random.choice(board.get_empty_squares())
        board.move(player_move[0], player_move[1], player)
        winner = board.check_win()
        if winner is None:
            other_move = random.choice(board.get_empty_squares())
            board.move(other_move[0], other_move[1],provided.switch_player(player))	
            winner = board.check_win()
    return 0



def mc_update_scores(scores, board, player):
    """
This function takes a grid of scores (a list of lists) with the same dimensions as the Tic-Tac-Toe board, a board from a completed game, 
and which player the machine player is. The function should score the completed board and update the scores grid. As the function updates the scores 
grid directly, it does not return anything,"""
    board_dim = board.get_dim()
    winner = board.check_win()
    machine_player_wins = winner==player
    if winner!=provided.DRAW:
        for row in range(board_dim):
            for col in range(board_dim):
                which_player=board.square(row,col)
                if machine_player_wins:
                    if which_player == provided.EMPTY:
                        pass
                    elif which_player == player:
                        scores[row][col] +=SCORE_CURRENT
                    else:
                        scores[row][col] -=SCORE_OTHER				
                else:
                    if which_player == provided.EMPTY:
                        pass
                    elif which_player == player:
                        scores[row][col] -=SCORE_CURRENT
                    else:
                        scores[row][col] +=SCORE_OTHER



def get_best_move(board, scores): 
    '''
This function takes a current board and a grid of scores. The function should find all of the empty 
squares with the maximum score and randomly return one of them as a (row, column) tuple. It is an error
to call this function with a board that has no empty squares (there is no possible next move), 
so your function may do whatever it wants in that case. The case where the board is full will not 
be tested.
'''
    empty_squares = board.get_empty_squares()
    print board
    maximum_value = float('-Infinity')
    row = empty_squares[0][0]
    col = empty_squares[0][1]
    for elem in empty_squares:
        scr = scores[elem[0]][elem[1]]
        if scr > maximum_value:
            row = elem[0]
            col = elem[1]
            maximum_value = scr
    return (row,col)


def mc_move(board, player, trials): 
    '''This function takes a current board, which player the machine player is, and the number of trials to run. 
The function should use the Monte Carlo simulation described above to return a move for the machine player in the form of a (row, column) tuple. 
Be sure to use the other functions you have written!'''
    board_dim = board.get_dim()
    scores = [[0 for _ in range(board_dim)] for _ in range(board_dim)]
    for _ in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    return get_best_move(board, scores)


#print get_best_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), [[1, 2, 3], [7, 8, 9], [4, 5, 6]]) 
#mc_update_scores([[0, 0, 0], [0, 0, 0], [0, 0, 0]], provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.PLAYERO]]), 3)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
