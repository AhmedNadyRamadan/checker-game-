# put all constants here to if i want change anything of them so will do it just one time
import pygame

WIDTH, HEIGHT = 700, 700  # the size of window
ROWS, COLS = 8, 8  # number of rows and columns
SQUARE_SIZE = WIDTH // COLS  # 87.5

# all rgb colors that will used
MAROON = (128, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
khaki = (240, 230, 140)
peru = (205, 133, 63)
saddle_brown = (139, 69, 19)
light_steel_blue = (176, 196, 222)
tan = (210, 180, 140)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))  # the style of king
# this photo "crown.png" made with photoshop to make it not have background color
