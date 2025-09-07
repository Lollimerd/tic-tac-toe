# constants.py
# Contains all game constants

# Screen dimensions
WIDTH, HEIGHT = 600, 600

# Board dimensions
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Line widths
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
CROSS_WIDTH = 25
CIRCLE_WIDTH = 15

# Spacing
SPACE = SQUARE_SIZE // 4
CIRCLE_RADIUS = SQUARE_SIZE // 3

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
WIN_COLOR = (255, 50, 50)
OVERLAY_BG_COLOR = (0, 0, 0, 180)
TEXT_COLOR = (255, 255, 255)