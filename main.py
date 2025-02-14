import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import pygame
import os

pygame.mixer.init()

# Проверка наличия файла с музыкой
if os.path.exists("background_music.mp3"):
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
else:
    print("Файл background_music.mp3 не найден. Музыка не будет воспроизводиться.")


def generate_math_problem(level):
    if level == 1:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operator = random.choice(["+", "-"])
        problem = f"{a} {operator} {b}"
        answer = eval(problem)
        return problem, answer
    elif level == 2:
        a = random.randint(10, 50)
        b = random.randint(10, 50)
        operator = random.choice(["+", "-", "*"])
        problem = f"{a} {operator} {b}"
        answer = eval(problem)
        return problem, answer
    elif level == 3:
        a = random.randint(50, 100)
        b = random.randint(50, 100)
        operator = random.choice(["+", "-", "*", "/"])
        problem = f"{a} {operator} {b}"
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
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики с математикой")
        self.root.geometry("400x500")
        self.level = 1
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.selected_cell = None
        self.correct_answer = None

        # Стартовое меню
        self.start_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)
        self.problem_frame = tk.Frame(self.root)

        # Виджеты для ввода примера
        self.problem_label = tk.Label(self.problem_frame, font=("Arial", 14), height=2)
        self.problem_label.pack(pady=5)
        self.answer_entry = tk.Entry(self.problem_frame, font=("Arial", 14), width=15)
        self.answer_entry.pack(pady=5)

        self.check_button = tk.Button(
            self.problem_frame, text="Проверить", font=("Arial", 12),
            command=self.check_answer
        )
        self.check_button.pack(pady=5)

        self.exit_button = tk.Button(
            self.problem_frame, text="Выход", font=("Arial", 12),
            command=self.root.quit
        )
        self.exit_button.pack(pady=5)

        self.problem_frame.pack_forget()

        # Создаем стартовые кнопки один раз
        self.create_start_widgets()

    def create_start_widgets(self):
        # Очищаем стартовый фрейм перед созданием кнопок
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        tk.Label(self.start_frame, text="Крестики-нолики", font=("Arial", 16)).pack(pady=10)
        tk.Button(
            self.start_frame, text="Играть с человеком", font=("Arial", 12),
            command=self.start_game
        ).pack(pady=10)
        tk.Button(
            self.start_frame, text="Уровень сложности", font=("Arial", 12),
            command=self.select_level
        ).pack(pady=10)
        tk.Button(
            self.start_frame, text="Настройки громкости", font=("Arial", 12),
            command=self.adjust_volume
        ).pack(pady=10)
        tk.Button(
            self.start_frame, text="Выход", font=("Arial", 12),
            command=self.root.quit
        ).pack(pady=10)

        self.start_frame.pack(pady=50)

    def adjust_volume(self):
        volume_window = tk.Toplevel(self.root)
        volume_window.title("Настройка громкости")
        volume_window.geometry("300x100")

        volume_label = tk.Label(volume_window, text="Установите громкость:", font=("Arial", 12))
        volume_label.pack(pady=10)

        volume_scale = tk.Scale(volume_window, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                                length=200, command=lambda value: pygame.mixer.music.set_volume(float(value)))
        volume_scale.set(pygame.mixer.music.get_volume())
        volume_scale.pack()

    def start_game(self):
        self.start_frame.pack_forget()
        self.problem_frame.pack_forget()
        self.game_frame.pack()
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.game_frame, text="", font=("Arial", 30), width=4, height=2,
                    command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        # Кнопка "Выход" во время игры
        self.exit_game_button = tk.Button(
            self.game_frame, text="Выход", font=("Arial", 12),
            command=self.reset_game
        )
        self.exit_game_button.grid(row=3, column=0, columnspan=3, pady=10)

    def toggle_board_state(self, active):
        state = tk.NORMAL if active else tk.DISABLED
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=state)

    def on_button_click(self, i, j):
        if self.board[i][j] != " ":
            return

        self.selected_cell = (i, j)
        problem, answer = generate_math_problem(self.level)
        self.correct_answer = answer

        # Возвращаем всплывающее окно для решения примера
        user_answer = self.ask_math_problem(problem)
        if user_answer is not None and user_answer == answer:
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)

            if check_win(self.board, self.current_player):
                messagebox.showinfo("Победа!", f"Победил {self.current_player}!")
                self.reset_game()
                return
            elif all(cell != " " for row in self.board for cell in row):
                messagebox.showinfo("Ничья!", "Игра окончена вничью!")
                self.reset_game()
                return

            # Переключаем игрока
            self.current_player = "O" if self.current_player == "X" else "X"
        else:
            messagebox.showinfo("Ошибка", "Неверный ответ! Ход переходит сопернику.")
            self.current_player = "O" if self.current_player == "X" else "X"

    def ask_math_problem(self, problem):
        try:
            user_input = simpledialog.askstring("Математический пример", f"Решите пример: {problem}")
            if user_input is None:  # Если пользователь нажал "Отмена"
                return None
            return float(user_input)
        except ValueError:
            messagebox.showinfo("Ошибка", "Введите число!")
            return None

    def check_answer(self):
        try:
            user_answer = float(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число!")
            return

        if user_answer == self.correct_answer:
            i, j = self.selected_cell
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)

            if check_win(self.board, self.current_player):
                messagebox.showinfo("Победа!", f"Победил {self.current_player}!")
                self.reset_game()
                return
            elif all(cell != " " for row in self.board for cell in row):
                messagebox.showinfo("Ничья!", "Игра окончена вничью!")
                self.reset_game()
                return

            self.current_player = "O" if self.current_player == "X" else "X"
            self.problem_frame.pack_forget()
            self.toggle_board_state(True)
        else:
            messagebox.showinfo("Ошибка", "Неверный ответ! Ход переходит сопернику.")
            self.current_player = "O" if self.current_player == "X" else "X"
            self.problem_frame.pack_forget()
            self.toggle_board_state(True)

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.problem_frame.pack_forget()
        self.start_frame.pack_forget()
        self.game_frame.pack_forget()
        self.create_start_widgets()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)

    def select_level(self):
        level = simpledialog.askinteger("Выбор уровня", "Выберите уровень сложности (1-3):", minvalue=1, maxvalue=3)
        if level is not None:  # Проверка на отмену
            self.level = level


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
