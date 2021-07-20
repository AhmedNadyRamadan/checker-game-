import pygame  # library of doing dames in python
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, peru  # call data from constants file
from .piece import Piece  # # call data from piece


def draw_squares(win):  # to draw the shape of board
    win.fill(BLACK)  # color of background
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):  # to move diagonal and up2 to make cell and cell no in row
            pygame.draw.rect(win, peru, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # draw rectangle in selected cells with color peru


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12  # number of pieces at first
        self.red_kings = self.white_kings = 0  # number of kings at first
        self.create_board()  # show the board without doing nothing

    def evaluate(self):  # to calculate the number of remaining pieces
        return self.white_left - self.red_left + self.white_kings - self.red_kings

    def get_all_pieces(self, color):  # to show all pieces from the same color after move of player
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:  # there are piece and have specific color
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):  # chang piece's location and increase the number of kings
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)  # exchange their positions

        if row == ROWS - 1 or row == 0:  # at the first (0) or the last (7) row
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:  # increase the number og kings based on it's color
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]  # to return the position of selected piece

    def create_board(self):  # put every piece in it's position before doing any move
        # hint (0,0) It's the top left piece in board
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):  # to put pieces at black cells
                    if row < 3:  # first three rows owns by white  pieces
                        self.board[row].append(Piece(row, col, WHITE))  # color of top pieces
                    elif row > 4:  # row number 5,6 and 7 owns by red pieces
                        self.board[row].append(Piece(row, col, RED))  # color of bottom pieces
                    else:
                        self.board[row].append(0)
                else:  # to don't show pieces at rows number 3,4
                    self.board[row].append(0)

    def draw(self, win):  # to show the main window
        draw_squares(win)  # win ---> window
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)  # put this piece in this location in main window "board"

    def remove(self, pieces):  # to hide piece after the player or computer eat it
        for piece in pieces:
            self.board[piece.row][piece.col] = 0  # hide it
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1  # decrease the number of remaining red pieces one
                else:
                    self.white_left -= 1  # decrease the number of remaining white pieces one

    def winner(self):  # determine the winner with it's remaining number of it's pieces
        if self.red_left <= 0:  # don't have any piece
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):  # to show the positions that can move to it
        moves = {}
        left = piece.col - 1  # move left
        right = piece.col + 1  # move right
        row = piece.row
                                              # I will not check red down 5 or 2 up white
        if piece.color == RED or piece.king:  # -3 to check 2 rows ,-1 to check one row  ,-1 one step up
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))  # diagonal left
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))  # diagonal right
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):  # determine when I can move left
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:   # no coulombs at left of this piece
                break

            current = self.board[r][left]
            if current == 0:    # empty cell
                if skipped and not last:   # I skipped this cell and no cell to stand in
                    break
                elif skipped:    # double eat happen
                    moves[(r, left)] = last + skipped   # move to next cell
                else:
                    moves[(r, left)] = last   # make this cell equal last move

                if last:  # check if I can make double eat or not
                    if step == -1:  # don't make any move
                        row = max(r - 3, 0)  # if double of red piece eat will move 2 rows up and if single eat will
                        # move 1 row up and if 0 I will still stand in my position
                    else:           # white piece eat
                        row = min(r + 3, ROWS)   # if double eat will move 2 rows and if single eat will move 1 row
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                    # to check if I can triple eat or more with giving currently position and check
                break
            elif current.color == color:  # 2 red pieces or two white pieces at the same diagonal next to them
                break
            # elif current.color != color:
            else:
                last = [current]   # stand in this position and flag it with last

            left -= 1  # piece was eaten

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            # elif current.color != color:
            else:
                last = [current]

            right += 1

        return moves
