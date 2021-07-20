from copy import deepcopy  # because I will need more copies of board "roots of minimax tree"
                           # when I make any change in the copy the other not change
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def minimax(position, depth, max_player, game):  # to take the decision and max_player to determine mini or max
    if depth == 0 or position.winner() is not None:  # the game continuous
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')   # make initial value to maximum evaluation with -infinite to take any value bigger
        best_move = None    # still not choose the best move
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth - 1, True, game)[0]  # because the return may will be 8 position need save
            maxEval = max(maxEval, evaluation)   # choose the best one
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:                # red player need to minimize the value
        minEval = float('inf')  # put initial very big positive number to choose any number smaller than it
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth - 1, False, game)[0]   # make minimization with false
            minEval = min(minEval, evaluation)   # choose the minimum
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def simulate_move(piece, move
                  , board, _, skip):   # to compare between the moves and choose the best
    board.move(piece, move[0], move[1])  # move[0]--->row and move[1]----->coulomb
    if skip:   # if I can eat
        board.remove(skip)   # so will take this move and remove skipped piece from the board

    return board


def get_all_moves(board, color, game):  # take a view of all possible moves to choose the best one
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)  # assign valid moves with all possible moves
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)  # draw the board after move
            temp_board = deepcopy(board)    # take a copy of the board
            temp_piece = temp_board.get_piece(piece.row, piece.col)  # assign the piece to make simulated move
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)   # new board after make this move
            moves.append(new_board)   # the the chosen piece in new position and draw the board

    return moves


def draw_moves(game, board, _):   # the shape of board after computer play
    board.draw(game.win)
    pygame.display.update()
    pygame.time.delay(100)   # time of thinking of computer
