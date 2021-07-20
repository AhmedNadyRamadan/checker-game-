import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax  # import             #

# import all files

FPS = 2  # the time of move

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')  # the outer of game with name checkers


def get_row_col_from_mouse(pos):   # to know which row and coulomb that piece stand
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True    # still show the board
    clock = pygame.time.Clock()
    game = Game(WIN)  # open the window of board

    while run:
        clock.tick(FPS)   # assign time of move

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 1, WHITE, game)
            game.ai_move(new_board)     # show board after move of white

        if game.winner() is not None:
            print(game.winner())
            run = False     # after win hide the board

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # shut down game if press quit
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)  # get the position that determine to move from the mouse
                game.select(row, col)

        game.update()

    pygame.quit()


main()
