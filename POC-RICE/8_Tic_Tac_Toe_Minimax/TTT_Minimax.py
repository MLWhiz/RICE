"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    
    empty_squares = board.get_empty_squares()
    if board.check_win():
        return SCORES[board.check_win()], (-1, -1)
    
    case = 'MIN'
    if player==provided.PLAYERX:
        case = 'MAX'

    scores = []
    moves = []
    for empty_sq in empty_squares:
        clone_board = board.clone()
        clone_board.move(empty_sq[0],empty_sq[1],player)
        score,_= mm_move(clone_board,provided.switch_player(player))
        if score == 1 and case =='MAX':
            return score,empty_sq
        if score == -1 and case == 'MIN':
            return score,empty_sq
        scores.append(score)
        moves.append(empty_sq)



    if player==provided.PLAYERX:
        best_move = None
        max_score = -2
        for ind in range(0,len(scores)):
            if scores[ind]>=max_score:
                max_score = scores[ind]
                best_move = moves[ind]
        return max(scores), best_move


    if player==provided.PLAYERO:
        best_move = None
        min_score = 4
        for ind in range(0,len(scores)):
            if scores[ind]<min_score:
                min_score = scores[ind]
                best_move = moves[ind]
        return min(scores), best_move

    

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), provided.PLAYERO)
#print mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX)