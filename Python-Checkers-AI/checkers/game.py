import pygame
from .constants import RED, WHITE, SQUARE_SIZE, tan
from checkers.board import Board


class Game:
    def __init__(self, win):  # constructor
        self._init()
        self.win = win

    def update(self):  # update the board after show hints
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)  # show small circle as a hint to help the player
        pygame.display.update()

    def _init(self):   # constructor
        self.selected = None
        self.board = Board()
        self.turn = RED  # to make all the program wait red player to play "choose who will start player or computer"
        self.valid_moves = {}

    def winner(self):  # return that the game end
        return self.board.winner()

    def reset(self):  # go the the start point again
        self._init()

    def select(self, row, col):  # select piece
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)  # recursion to select another piece

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:  # the piece moves if it it's turn to move
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)  # where he can move
            return True

        return False   # It's can't move

    def _move(self, row, col):   # move piece to the new position and remove it from old position
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]  # the old chosen piece
            if skipped:
                self.board.remove(skipped)  # remove old piece after the move
            self.change_turn()  # turn if from red (start) to white (second player computer) or otherwise
        else:
            return False

        return True

    def draw_valid_moves(self, moves):  # to put a pointer to show available moves right or left diagonal
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, tan,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
            # two show hint with tan color for available diagonal moves "hint is a circle with radius 10

    def change_turn(self):      # to chang turn after every movement
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
