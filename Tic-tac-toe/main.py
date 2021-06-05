import pygame
import numpy as np

pygame.init()
# ---------
# CONSTANTS
# ---------
WIDTH, HEIGHT  = 430, 515
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = (WIDTH-15) // BOARD_COLUMNS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15 
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

WINNER_FONT = pygame.font.SysFont('comicsans', 120)
TURN_FONT = pygame.font.SysFont('comicsans', 70)

#-----------
# RGB COLORS 
#-----------
BLACK = (0, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (255, 255, 255)
CROSS_COLOR = (66, 66, 66)

# ------
# SCREEN
# ------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC-TAC-TOE")
screen.fill(BG_COLOR)

# -------------
# CONSOLE BOARD
# -------------
board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))

# ---------
# FUNCTIONS
# ---------
def draw_lines():
    ''' FOR BORDERS'''
    pygame.draw.line(screen, LINE_COLOR, (0, 0), (0, HEIGHT), 2 * LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 0), (WIDTH, 0), 2 *LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH, 0), (WIDTH, HEIGHT), 2 * LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT), (WIDTH, HEIGHT), 2 * LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 85), (WIDTH, 85), LINE_WIDTH)


    ''' FOR HASHTAG # '''
    # HORIONTAL 1
    pygame.draw.line(screen, LINE_COLOR, (15, SQUARE_SIZE + 85), (WIDTH, SQUARE_SIZE + 85), LINE_WIDTH)
    # HORIZONTAL 2
    pygame.draw.line(screen, LINE_COLOR, (15, 2 * SQUARE_SIZE + 85), (WIDTH, 2 * SQUARE_SIZE + 85), LINE_WIDTH)
    # VERTICAL 1
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 85 ), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # VERTICAL 2
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 85), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):

            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR,(
                    int(col * SQUARE_SIZE + SQUARE_SIZE // 2),int(
                        row * SQUARE_SIZE + SQUARE_SIZE // 2 + 85)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR,(
                    col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 85),(col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE + 85),CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,(
                    col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE + 85 ),(col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 85),CROSS_WIDTH)


def mark_square(row, col ,player):
    board[row][col] = player
    
def availiable_square(row, col):
    return board[row] [col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row] [col] == 0 :
                return False
    return True


def check_win(player):
    # vertical win check
    for col in range(BOARD_COLUMNS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # asc diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal_line(player)
        return True

    # desc diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal_line(player)
        return True

    return False 
    
def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2 

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 100), (posX, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2 + 85

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR 
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH)


def draw_asc_diagonal_line(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (25, HEIGHT - 30), (WIDTH - 5 , 100 ), WIN_LINE_WIDTH)


def draw_desc_diagonal_line(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (25, 100), (WIDTH - 25, HEIGHT - 25), WIN_LINE_WIDTH)


def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            board[row][col] = 0
    draw_turn("O's turns")



def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, BLACK)
    #screen.fill(BG_COLOR)
    screen.blit(winner_text, (WIDTH/2 - winner_text.get_width() /
                         2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()


def draw_turn(text):
    turn_text = TURN_FONT.render(text, 1, BLACK)
    #screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BG_COLOR, pygame.Rect(20, 20, WIDTH-40, 60))
    screen.blit(turn_text, (WIDTH/2 - turn_text.get_width() / 2, 30))

draw_turn("O's turns")
draw_lines()

# -------VARIABLES-------

player = 1
running = True

#------------------
#  MAIN LOOP
#------------------

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            runinng = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN :

            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y

            clicked_row = int((mouseY-85) // SQUARE_SIZE)
            clicked_col = int((mouseX-15) // SQUARE_SIZE)
            print(clicked_row, clicked_col )

            if availiable_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if player == 1 :
                    pl = "O"
                    p = "X"
                else:
                    pl = "X"
                    p = "O" 

                draw_turn(p+"'s turns")
                draw_figures()

                if check_win(player):
                    draw_winner(pl+" WIN")
                    pygame.time.delay(3000)
                    player = 1
                    restart()
                player = player % 2 + 1
            #else:
            #   draw_winner("TIE !!")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1

    pygame.display.update()