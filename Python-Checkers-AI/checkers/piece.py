from .constants import SQUARE_SIZE, GREY, CROWN
import pygame


class Piece:
    PADDING = 15  # put the circle in the middle with padding and out_circle
    OUTLINE = 3  # draw circle outer every piece

    def __init__(self, row, col, color):   # constructor
        self.row = row
        self.col = col
        self.color = color
        self.king = False  # the shape of pieces
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):  # put the circle in the middle of square of every row
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):  # to turn piece to king
        self.king = True

    def draw(self, win):  # shape of piece "circle"
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)  # to draw circle out of piece
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)  # to double the circle around piece
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))
            # to put the photo of crown in the middle and above of piece

    def move(self, row, col):  # to calculate the position of selected piece
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):   # destructor
        return str(self.color)  # calculate the representation of color
