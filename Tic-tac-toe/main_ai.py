import pygame
import random
import numpy as np


pygame.init()

# Variables


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
                pygame.draw.line(screen, CROSS_COLOR,(
                    col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 85),(col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE + 85),CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,(
                    col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE + 85 ),(col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 85),CROSS_WIDTH)

            elif board[row][col] == 2:
                possibility_human_win()

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
    global player
    player = 1
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
    pygame.time.delay(3)
    restart()


def draw_turn(text):
    turn_text = TURN_FONT.render(text, 1, BLACK)
    #screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BG_COLOR, pygame.Rect(20, 20, WIDTH-40, 60))
    screen.blit(turn_text, (WIDTH/2 - turn_text.get_width() / 2, 30))

def com_move(row, col):

    # figure
    pygame.draw.circle(screen, CIRCLE_COLOR,(
    int(col * SQUARE_SIZE + SQUARE_SIZE // 2),int(
    row * SQUARE_SIZE + SQUARE_SIZE // 2 + 85)), CIRCLE_RADIUS, CIRCLE_WIDTH)


def random_move():
    ran = True
    while ran:
        a = random.randint(0, 2)
        b = random.randint(0, 2)

        if availiable_square(a ,b):
            mark_square(a, b, player)
            com_move(a,b)
            ran = False


def possibility_human_win():
    poss_player = 0
    d_row = None
    d_row = None
    # Vertical possibility check
    for col in range(3):
        row1 = 0
        row2 = 1
        row3 = 2

        if board[row1][col] == 1 and board[row2][col] == 1 and board[row3][col] == 2:
            break
        elif board[row1][col] == 1 and board[row2][col] == 1:
            poss_player += 1
            d_row = 2
            d_col = col

        if board[row2][col] == 1 and board[row3][col] == 1 and board[row1][col] == 2 : 
            break
        elif board[row2][col] == 1 and board[row3][col] == 1:
            poss_player += 1
            d_row = 0
            d_col = col
            
        if board[row1][col] == 1 and board[row3][col] == 1 and board[row2][col] == 2:
            break 
        elif board[row1][col] == 1 and board[row3][col] == 1 :
            poss_player += 1
            d_row = 1
            d_col = col

    # Horizontal possibility check
    for row in range(3):
        col1 = 0
        col2 = 1
        col3 = 2

        if board[row][col1] == 1 and board[row][col2] == 1 and board[row][col3] == 2:
            break
        elif board[row][col1] == 1 and board[row][col2] == 1:
            poss_player += 1
            d_row = row
            d_col = 2

        if board[row][col2] == 1 and board[row][col3] == 1 and board[row][col1] == 2 : 
            break
        elif board[row][col2] == 1 and board[row][col3] == 1:
            poss_player += 1
            d_row = row
            d_col = 0
            
        if board[row][col1] == 1 and board[row][col3] == 1 and board[row][col2] == 2:
            break 
        elif board[row][col1] == 1 and board[row][col3] == 1 :
            poss_player += 1
            d_row = row
            d_col = 1

    if d_row == None and d_col == None:
        random_move()
    else:
        com_move(d_row, d_col)
        
    '''
    #  asc diagonal possibility check
    if board[2][0] == player and board[1][1] == player or board[1][1] == player and board[0][2] == player or board[2][0] == player and board[0][2] == player:
        pass

    #  asc diagonal possibility check
    if board[0][0] == player and board[1][1] == player or board[1][1] == player and board[2][2] == player or board[0][0] == player and board[2][2] == player:
        pass
    '''

draw_turn("X's turns")
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
            if clicked_row == - 1:
                continue

            if availiable_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if player == 1 :
                    pl = "X"
                    p = "O"
                else:
                    pl = "O"
                    p = "X" 

                draw_turn(p+"'s turns")

                if check_win(player):
                    draw_winner(pl+" WIN")
                player = player % 2 + 1

            else :
               draw_winner("TIE !!")
        draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

    pygame.display.update()