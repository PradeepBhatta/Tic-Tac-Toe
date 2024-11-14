import pygame, sys
import numpy as np
import copy
import random

# General Setup
pygame.init()
clock = pygame.time.Clock()

# CONSTANTS
WIDTH, HEIGHT = 750, 500
LINE_WIDTH = 8
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = 100
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

WINNER_FONT = pygame.font.SysFont('comicsans', 120)
TURN_FONT = pygame.font.SysFont('comicsans', 70)
BUTTON_FONT = pygame.font.SysFont('comicsans', 20)

# RGB COLORS
BLACK = (0, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (255, 255, 255)
CROSS_COLOR = (66, 66, 66)
DROPDOWN_BG_COLOR = (20, 100, 100)

# SCREEN
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC-TAC-TOE")
screen.fill(BG_COLOR)

# Initial Game State
game_state = 'game_PvAI'
difficulty = 'medium'
dropdown_open = False
dropdown_rect = pygame.Rect(30, 20, 150, 150)  # Enlarged dropdown area

# Helper Function to Draw Text
def draw_text(text, font, color, pos):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, text_surface.get_rect(center=pos))

# Dropdown Menu Function
def draw_dropdown():
    # Draw the dropdown button and current selection
    pygame.draw.rect(screen, DROPDOWN_BG_COLOR, (30, 20, 150, 30), 0, 5)
    current_mode = difficulty.capitalize() if game_state == "game_PvAI" else "Friend"
    draw_text(current_mode, BUTTON_FONT, BLACK, (105, 35))

    if dropdown_open:
        # Draw the dropdown menu options
        pygame.draw.rect(screen, DROPDOWN_BG_COLOR, (30, 50, 150, 150), 0, 5)
        options = ["Easy", "Medium", "Impossible", "Play against a Friend"]
        for i, option in enumerate(options):
            option_pos = (105, 65 + i * 20)
            draw_text(option, BUTTON_FONT, BLACK, option_pos)
            # Draw tick mark next to the selected option
            if option.lower() == difficulty or (option == "Play against a Friend" and game_state == "game_PvP"):
                pygame.draw.circle(screen, BLACK, (45, 65 + i * 20), 4)

# Game Class
class Game:
    def __init__(self):
        self.board = Board()
        self.player = 1
        self.game_over = False
        self.animation_complete = False
        self.current_length = 0
        self.grid_lines = [
            ((225, SQUARE_SIZE * 2), (SQUARE_SIZE * 3 + 225, SQUARE_SIZE * 2)),
            ((225, SQUARE_SIZE * 3), (SQUARE_SIZE * 3 + 225, SQUARE_SIZE * 3)),
            ((SQUARE_SIZE + 225, SQUARE_SIZE), (SQUARE_SIZE + 225, SQUARE_SIZE * 4)),
            ((2 * SQUARE_SIZE + 225, SQUARE_SIZE), (2 * SQUARE_SIZE + 225, SQUARE_SIZE * 4)),
        ]

    def animate_lines(self):
        max_length = SQUARE_SIZE * 3
        for start_pos, end_pos in self.grid_lines:
            self.draw_line_segment(start_pos, end_pos, self.current_length)
        self.current_length += 15  # Animation speed
        if self.current_length > max_length:
            self.animation_complete = True

    def draw_line_segment(self, start_pos, end_pos, current_length):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dx, dy = x2 - x1, y2 - y1
        total_length = np.sqrt(dx ** 2 + dy ** 2)
        half_length = min(current_length / 2, total_length / 2)
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        start_x = center_x - (dx * half_length / total_length)
        start_y = center_y - (dy * half_length / total_length)
        end_x = center_x + (dx * half_length / total_length)
        end_y = center_y + (dy * half_length / total_length)
        pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), LINE_WIDTH)
        pygame.draw.circle(screen, LINE_COLOR, (int(start_x), int(start_y)), LINE_WIDTH // 2)
        pygame.draw.circle(screen, LINE_COLOR, (int(end_x), int(end_y)), LINE_WIDTH // 2)

    def draw_lines(self):
        if not self.animation_complete:
            self.animate_lines()
        else:
            for start_pos, end_pos in self.grid_lines:
                pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, LINE_WIDTH)

    def draw_figures(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if self.board.squares[row][col] == 1:
                    pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2 + 225), int(row * SQUARE_SIZE + SQUARE_SIZE // 2 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board.squares[row][col] == 2:
                    pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE + 225, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 100), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + 225, row * SQUARE_SIZE + SPACE + 100), CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE + 225, row * SQUARE_SIZE + SPACE + 100), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + 225, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 100), CROSS_WIDTH)

    def restart(self):
        self.player = 1
        self.game_over = False
        self.animation_complete = False
        self.current_length = 0  # Reset animation length
        self.board.squares.fill(0)
        screen.fill(BG_COLOR, (225, 100, SQUARE_SIZE * 3, SQUARE_SIZE * 3 + 100))  # Clear only the game area
        self.draw_turn("O's turn")

    def draw_winner(self, text):
        winner_text = WINNER_FONT.render(text, 1, BLACK)
        screen.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)
        self.restart()

    def draw_turn(self, text):
        turn_text = TURN_FONT.render(text, 1, BLACK)
        pygame.draw.rect(screen, BG_COLOR, pygame.Rect(20, 20, WIDTH - 40, 60))
        screen.blit(turn_text, (WIDTH / 2 - turn_text.get_width() / 2, 30))

# Board Class
class Board:
    def __init__(self):
        self.squares = np.zeros((BOARD_ROWS, BOARD_COLUMNS))

    def mark_square(self, row, col, player):
        self.squares[row][col] = player

    def available_square(self, row, col):
        return self.squares[row][col] == 0

    def is_board_full(self):
        return not np.any(self.squares == 0)

    def check_win(self):
        for col in range(BOARD_COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        for row in range(BOARD_ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[2][0]
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[0][0]
        return 0

# AI Class
class AI:
    def __init__(self, level='medium'):
        self.level = level

    def terminal(self, board):
        return board.check_win() != 0 or board.is_board_full()

    def utility(self, board):
        winner = board.check_win()
        if winner == 1:
            return 10
        elif winner == 2:
            return -10
        return 0

    def actions(self, board):
        remaining = set()
        for x in range(BOARD_ROWS):
            for y in range(BOARD_COLUMNS):
                if board.squares[x][y] == 0:
                    remaining.add((x, y))
        return remaining

    def result(self, board, action, player):
        new_board = copy.deepcopy(board)
        new_board.squares[action[0]][action[1]] = player
        return new_board

    def minimax(self, board, depth, isMax, alpha, beta):
        if self.terminal(board):
            return self.utility(board)

        if isMax:
            maxEval = -float('inf')
            for action in self.actions(board):
                eval = self.minimax(self.result(board, action, 1), depth + 1, False, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for action in self.actions(board):
                eval = self.minimax(self.result(board, action, 2), depth + 1, True, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def findBestMove(self, board):
        # AI strategy based on difficulty level
        if self.level == 'easy':
            return random.choice(list(self.actions(board)))
        elif self.level == 'medium':
            # Medium: make a strategic choice randomly or use minimax at depth 1 or 2
            if random.random() > 0.5:
                return random.choice(list(self.actions(board)))
            else:
                # Slightly strategic move, depth 2 minimax
                bestMove = None
                bestValue = float('inf')
                for action in self.actions(board):
                    moveValue = self.minimax(self.result(board, action, 2), 2, True, -float('inf'), float('inf'))
                    if moveValue < bestValue:
                        bestValue = moveValue
                        bestMove = action
                return bestMove
        else:  # Impossible
            bestMove = None
            bestValue = float('inf')
            for action in self.actions(board):
                moveValue = self.minimax(self.result(board, action, 2), 0, True, -float('inf'), float('inf'))
                if moveValue < bestValue:
                    bestValue = moveValue
                    bestMove = action
            return bestMove

# GameState Class
class GameState:
    def __init__(self, game_state, difficulty):
        self.state = game_state
        self.difficulty = difficulty
        self.game = Game()
        self.ai = AI(difficulty)

    def main_game(self):
        pass

    def state_manager(self, game_state):
        self.state = game_state
        self.game.draw_lines()
        self.game.draw_turn("O's turn")
        if self.game.animation_complete:
            self.game.draw_figures()
        self.ga()

    def ga(self):
        global event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.restart()

        if event.type == pygame.MOUSEBUTTONDOWN and not self.game.game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = int((mouseY - 100) // SQUARE_SIZE)
            clicked_col = int((mouseX - 225) // SQUARE_SIZE)

            if 0 <= clicked_row < BOARD_ROWS and 0 <= clicked_col < BOARD_COLUMNS and self.game.board.available_square(clicked_row, clicked_col):
                self.game.board.mark_square(clicked_row, clicked_col, 1)
                self.game.draw_figures()
                if self.game.board.check_win() == 1:
                    self.game.game_over = True
                    self.game.draw_winner("O WINS")
                elif self.game.board.is_board_full():
                    self.game.game_over = True
                    self.game.draw_winner("TIE!")
                else:
                    self.game.player = 2
                    self.game.draw_turn("X's turn")
                    if not self.game.board.is_board_full():
                        move = self.ai.findBestMove(self.game.board)
                        if move:
                            self.game.board.mark_square(move[0], move[1], self.game.player)
                            self.game.draw_figures()
                            if self.game.board.check_win() == 2:
                                self.game.game_over = True
                                self.game.draw_winner("X WINS")
                            elif self.game.board.is_board_full():
                                self.game.game_over = True
                                self.game.draw_winner("TIE!")
                    self.game.player = 1
                    self.game.draw_turn("O's turn")

g = GameState(game_state, difficulty)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if dropdown_rect.collidepoint(mouse_x, mouse_y):
                dropdown_open = not dropdown_open
                screen.fill(BG_COLOR, dropdown_rect)
                draw_dropdown()
                pygame.display.update(dropdown_rect)
            elif dropdown_open:
                if 50 <= mouse_y < 70:
                    difficulty, game_state = "easy", "game_PvAI"
                    g = GameState(game_state, difficulty)
                elif 70 <= mouse_y < 90:
                    difficulty, game_state = "medium", "game_PvAI"
                    g = GameState(game_state, difficulty)
                elif 90 <= mouse_y < 110:
                    difficulty, game_state = "impossible", "game_PvAI"
                    g = GameState(game_state, difficulty)
                elif 110 <= mouse_y < 130:
                    game_state = "game_PvP"
                    g = GameState(game_state, difficulty)
                dropdown_open = False
                screen.fill(BG_COLOR, dropdown_rect)
                draw_dropdown()
                pygame.display.update(dropdown_rect)
        g.state_manager(game_state)
    draw_dropdown()
    pygame.display.flip()
    clock.tick(30)

