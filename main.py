import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack()

        self.stop_button = tk.Button(self.root, text="Stop Game", command=self.stop_game)
        self.stop_button.pack()

        self.size = 20
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'Right'
        self.food = self.create_food()

        self.game_over = False
        self.paused = False
        self.score = 0
        self.record = 0
        self.menu_open = None  # Используем вместо флага для хранения окна меню

        self.root.bind("<KeyPress>", self.change_direction)
        self.update_game()

    def center_window(self, window, width=300, height=200):
        """Функция для центрирования окна на экране"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def start_menu(self):
        if not self.menu_open:  # Проверяем, что меню еще не открыто
            self.canvas.delete("all")
            self.menu_open = tk.Toplevel(self.root)
            self.menu_open.title("Menu")
            self.center_window(self.menu_open, 300, 200)  # Центрируем окно меню

            self.menu_open.protocol("WM_DELETE_WINDOW", self.close_menu)

            tk.Label(self.menu_open, text="Select Field Size:").pack()
            tk.Button(self.menu_open, text="Small", command=lambda: self.start_game(200)).pack()
            tk.Button(self.menu_open, text="Medium", command=lambda: self.start_game(400)).pack()
            tk.Button(self.menu_open, text="Large", command=lambda: self.start_game(600)).pack()

            tk.Label(self.menu_open, text=f"Record: {self.record}").pack()
            tk.Button(self.menu_open, text="Exit", command=self.root.quit).pack()

    def close_menu(self):
        if self.menu_open:
            self.menu_open.destroy()
            self.menu_open = None

    def start_game(self, size):
        self.close_menu()  # Закрываем меню при старте игры
        self.canvas.config(width=size, height=size)
        self.root.update_idletasks()

        self.size = size // 20
        self.snake = [(size // 2, size // 2), (size // 2 - 20, size // 2), (size // 2 - 40, size // 2)]
        self.food = self.create_food()
        self.direction = 'Right'
        self.game_over = False
        self.paused = False
        self.score = 0
        self.update_game()

    def create_food(self):
        max_x = (self.canvas.winfo_width() // self.size) - 1
        max_y = (self.canvas.winfo_height() // self.size) - 1
        if max_x > 0 and max_y > 0:
            while True:
                x = random.randint(0, max_x) * self.size
                y = random.randint(0, max_y) * self.size
                if (x, y) not in self.snake:
                    return x, y
        return 0, 0

    def change_direction(self, event):
        opposite_directions = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
        if event.keysym in ['Left', 'Right', 'Up', 'Down']:
            if self.direction != opposite_directions.get(event.keysym):
                self.direction = event.keysym

    def update_game(self):
        if not self.game_over and not self.paused:
            self.move_snake()
            self.check_collisions()
            self.update_canvas()
        self.root.after(300, self.update_game)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Left':
            head_x -= self.size
        elif self.direction == 'Right':
            head_x += self.size
        elif self.direction == 'Up':
            head_y -= self.size
        elif self.direction == 'Down':
            head_y += self.size

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.create_food()
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_y < 0 or head_x >= self.canvas.winfo_width() or head_y >= self.canvas.winfo_height():
            self.game_over = True
        if len(self.snake) != len(set(self.snake)):
            self.game_over = True

        if self.game_over:
            self.record = max(self.record, self.score)
            self.show_game_over_menu()

    def update_canvas(self):
        self.canvas.delete("all")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill="green")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + self.size, self.food[1] + self.size, fill="red")

    def stop_game(self):
        if not self.menu_open:
            self.paused = True
            self.menu_open = tk.Toplevel(self.root)
            self.menu_open.title("Pause Menu")
            self.center_window(self.menu_open, 300, 200)

            self.menu_open.protocol("WM_DELETE_WINDOW", self.close_menu)

            tk.Label(self.menu_open, text="Game Paused").pack()
            tk.Button(self.menu_open, text="Continue", command=self.resume_game).pack()
            tk.Button(self.menu_open, text="Main Menu", command=self.back_to_menu).pack()
            tk.Button(self.menu_open, text="Exit", command=self.root.quit).pack()

    def resume_game(self):
        self.close_menu()
        self.paused = False

    def back_to_menu(self):
        self.close_menu()
        self.paused = False
        self.start_menu()

    def show_game_over_menu(self):
        if not self.menu_open:
            self.menu_open = tk.Toplevel(self.root)
            self.menu_open.title("Game Over")
            self.center_window(self.menu_open, 300, 200)

            self.menu_open.protocol("WM_DELETE_WINDOW", self.close_menu)

            tk.Label(self.menu_open, text="Game Over!").pack()
            tk.Label(self.menu_open, text=f"Score: {self.score}").pack()
            tk.Button(self.menu_open, text="Main Menu", command=self.back_to_menu).pack()
            tk.Button(self.menu_open, text="Exit", command=self.root.quit).pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    game.start_menu()
    root.mainloop()
