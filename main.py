import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Крестики-нолики с математикой')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


def generate_math_problem(level):
    if level == 1:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operator = random.choice(['+', '-'])
        problem = f'{a} {operator} {b}'
        answer = eval(problem)
        return problem, answer
    elif level == 2:
        a = random.randint(10, 50)
        b = random.randint(10, 50)
        operator = random.choice(['+', '-', '*'])
        problem = f'{a} {operator} {b}'
        answer = eval(problem)
        return problem, answer
    elif level == 3:
        a = random.randint(50, 100)
        b = random.randint(50, 100)
        operator = random.choice(['+', '-', '*', '/'])
        problem = f'{a} {operator} {b}'
        answer = eval(problem)
        return problem, answer


def check_win(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False


class TicTacToe:
    def __init__(self):
        self.level = 1
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.selected_cell = None
        self.correct_answer = None
        self.show_problem = False
        self.problem_text = ''
        self.user_input = ''
        self.game_over = False
        self.in_menu = True
        self.volume = 0.5

    def draw_board(self):
        screen.fill(WHITE)
        for i in range(1, 3):
            pygame.draw.line(screen, BLACK, (WIDTH // 3 * i, 0), (WIDTH // 3 * i, HEIGHT - 100), 2)
            pygame.draw.line(screen, BLACK, (0, (HEIGHT - 100) // 3 * i), (WIDTH, (HEIGHT - 100) // 3 * i), 2)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'X':
                    pygame.draw.line(screen, RED, (j * WIDTH // 3 + 20, i * (HEIGHT - 100) // 3 + 20),
                                     ((j + 1) * WIDTH // 3 - 20, (i + 1) * (HEIGHT - 100) // 3 - 20), 2)
                    pygame.draw.line(screen, RED, ((j + 1) * WIDTH // 3 - 20, i * (HEIGHT - 100) // 3 + 20),
                                     (j * WIDTH // 3 + 20, (i + 1) * (HEIGHT - 100) // 3 - 20), 2)
                elif self.board[i][j] == 'O':
                    pygame.draw.circle(screen, BLUE,
                                       (j * WIDTH // 3 + WIDTH // 6, i * (HEIGHT - 100) // 3 + (HEIGHT - 100) // 6),
                                       WIDTH // 8, 2)

        if self.show_problem:
            problem_surface = font.render(self.problem_text, True, BLACK)
            screen.blit(problem_surface, (20, HEIGHT - 80))
            input_surface = font.render(self.user_input, True, BLACK)
            screen.blit(input_surface, (20, HEIGHT - 40))

    def draw_menu(self):
        screen.fill(WHITE)
        title_surface = font.render('Крестики-нолики с математикой', True, BLACK)
        screen.blit(title_surface, (20, 20))

        play_button = pygame.Rect(100, 100, 200, 50)
        pygame.draw.rect(screen, GRAY, play_button)
        play_text = font.render('Играть', True, BLACK)
        screen.blit(play_text, (150, 115))

        level_button = pygame.Rect(100, 170, 200, 50)
        pygame.draw.rect(screen, GRAY, level_button)
        level_text = font.render(f'Уровень: {self.level}', True, BLACK)
        screen.blit(level_text, (140, 185))

        volume_button = pygame.Rect(100, 240, 200, 50)
        pygame.draw.rect(screen, GRAY, volume_button)
        volume_text = font.render(f'Громкость: {int(self.volume * 100)}%', True, BLACK)
        screen.blit(volume_text, (120, 255))

        return play_button, level_button, volume_button

    def handle_click(self, pos):
        if self.show_problem:
            return

        x, y = pos
        row = y // ((HEIGHT - 100) // 3)
        col = x // (WIDTH // 3)

        if self.board[row][col] == ' ':
            self.selected_cell = (row, col)
            problem, answer = generate_math_problem(self.level)
            self.correct_answer = answer
            self.problem_text = f'Решите пример: {problem}'
            self.show_problem = True

    def handle_input(self, event):
        if event.key == pygame.K_RETURN:
            try:
                user_answer = float(self.user_input)
                if user_answer == self.correct_answer:
                    row, col = self.selected_cell
                    self.board[row][col] = self.current_player
                    if check_win(self.board, self.current_player):
                        self.game_over = True
                        self.show_problem = False
                        self.problem_text = f'Победил {self.current_player}!'
                    elif all(cell != ' ' for row in self.board for cell in row):
                        self.game_over = True
                        self.show_problem = False
                        self.problem_text = 'Ничья!'
                    else:
                        self.current_player = 'O' if self.current_player == 'X' else 'X'
                else:
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.show_problem = False
                self.user_input = ''
            except ValueError:
                self.problem_text = 'Ошибка! Введите число.'
        elif event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        else:
            self.user_input += event.unicode

    def reset_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.show_problem = False
        self.problem_text = ''
        self.user_input = ''


def main():
    game = TicTacToe()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.in_menu:
                    play_button, level_button, volume_button = game.draw_menu()
                    if play_button.collidepoint(event.pos):
                        game.in_menu = False
                    elif level_button.collidepoint(event.pos):
                        game.level = (game.level % 3) + 1
                    elif volume_button.collidepoint(event.pos):
                        game.volume = (game.volume + 0.1) % 1.1
                        pygame.mixer.music.set_volume(game.volume)
                elif not game.game_over:
                    game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN and game.show_problem:
                game.handle_input(event)
            elif event.type == pygame.KEYDOWN and game.game_over:
                if event.key == pygame.K_r:
                    game.reset_game()
                    game.in_menu = True

        if game.in_menu:
            game.draw_menu()
        else:
            game.draw_board()
            if game.game_over:
                game_over_surface = font.render(game.problem_text, True, BLACK)
                screen.blit(game_over_surface, (20, HEIGHT - 40))
                restart_surface = small_font.render('Нажмите R для рестарта', True, BLACK)
                screen.blit(restart_surface, (20, HEIGHT - 20))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()