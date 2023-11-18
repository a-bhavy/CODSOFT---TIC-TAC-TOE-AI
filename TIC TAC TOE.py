import pygame
import sys
import random
from pygame.locals import *

# Board Constants
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 3, 3
SQSIZE = WIDTH // COLS

# Color Constants
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CROSS_COLOR = (0, 0, 0)
CIRC_COLOR = (0, 0, 0)

# Initializing pygame

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

# Initializing the board

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
current_player = 1  # 1 for X, 2 for O
game_over = False
# To keep track of the winner
winner = None 

# Function to display the grid
def display_board():
    for row in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQSIZE), (WIDTH, row * SQSIZE), 2)
    for col in range(1, COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQSIZE, 0), (col * SQSIZE, HEIGHT), 2)

# Function to display X and O
def display_xo():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:
                x = col * SQSIZE + SQSIZE // 2
                y = row * SQSIZE + SQSIZE // 2
                pygame.draw.line(screen, CROSS_COLOR, (x - 50, y - 50), (x + 50, y + 50), 8)
                pygame.draw.line(screen, CROSS_COLOR, (x - 50, y + 50), (x + 50, y - 50), 8)
            elif board[row][col] == 2:
                x = col * SQSIZE + SQSIZE // 2
                y = row * SQSIZE + SQSIZE // 2
                pygame.draw.circle(screen, CIRC_COLOR, (x, y), 50, 8)

# Function for checking a win
def check_win(player, board):
    for row in range(ROWS):
        if all(board[row][col] == player for col in range(COLS)):
            return [(0, row), (COLS - 1, row)]
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            return [(col, 0), (col, ROWS - 1)]
    if all(board[i][i] == player for i in range(3)):
        return [(0, 0), (COLS - 1, ROWS - 1)]
    if all(board[i][2 - i] == player for i in range(3)):
        return [(COLS - 1, 0), (0, ROWS - 1)]
    return None

# Function for checking a draw
def check_draw(board):
    return all(cell != 0 for row in board for cell in row)

# Function to reset the game
def reset_game():
    global board, current_player, game_over, winner 
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    current_player = 1
    game_over = False
    winner = None


# Function for the AI player move which is unbeatable using minimax with alpha-beta pruning)
def ai_move(board, player):
    def minimax(board, depth, maximizing_player, alpha, beta):
        if check_win(1, board):
            return -1
        if check_win(2, board):
            return 1
        if check_draw(board):
            return 0

        if maximizing_player:
            max_eval = -float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] == 0:
                        board[row][col] = 2
                        eval = minimax(board, depth + 1, False, alpha, beta)
                        board[row][col] = 0
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] == 0:
                        board[row][col] = 1
                        eval = minimax(board, depth + 1, True, alpha, beta)
                        board[row][col] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    best_eval = -float('inf')
    best_move = None

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                eval = minimax(board, 0, False, -float('inf'), float('inf'))
                board[row][col] = 0
                if eval > best_eval:
                    best_eval = eval
                    best_move = (row, col)

    return best_move

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            elif current_player == 1:
                col = event.pos[0] // SQSIZE
                row = event.pos[1] // SQSIZE

                if board[row][col] == 0:
                    board[row][col] = current_player
                    win_coords = check_win(current_player, board)
                    if win_coords:
                        game_over = True
                        winner = current_player
                        
                    elif check_draw(board):
                        game_over = True
                    current_player = 3 - current_player  # Switch players

    if not game_over and current_player == 2:
        ai_row, ai_col = ai_move(board, 2)
        if ai_row is not None:
            board[ai_row][ai_col] = current_player
            win_coords = check_win(current_player, board)
            if win_coords:
                game_over = True
                winner = current_player
                
            elif check_draw(board):
                game_over = True
            current_player = 3 - current_player  # Switch players

    screen.fill(WHITE)
    display_board()
    display_xo()

    if winner is not None:
        font = pygame.font.Font(None, 99)
        if winner == 1:
            result_text = font.render("Player X wins", True,(255,0,0) )
        else:
            result_text = font.render("Player O wins", True,(255,0,0) )
        
        text_rect = result_text.get_rect()

            # Set the center coordinates of the text rectangle to the center of the screen
        text_rect.center = (WIDTH // 2.17, HEIGHT // 1.9 )

            # Blit the text surface to the screen using the updated rectangle
        screen.blit(result_text, text_rect.topleft)


    pygame.display.update()
