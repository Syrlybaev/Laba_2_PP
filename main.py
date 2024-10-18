import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        #создание окна и названия
        self.root = root
        self.root.title("Snake Game")
        #
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack()

        self.stop_button = tk.Button(self.root, text="Stop Game", command=self.stop_game)
        self.stop_button.pack()

        self.size = 20  # размер одной клетки змейки
        self.snake = [(100, 100), (80, 100), (60, 100)]  # начальная позиция змейки
        self.direction = 'Right'  # начальное направление движения
        self.food = self.create_food()

        self.game_over = False
        self.paused = False
        self.score = 0
        self.record = 0

        self.root.bind("<KeyPress>", self.change_direction)
        self.update_game()

    def start_menu(self):
        self.canvas.delete("all")
        menu = tk.Toplevel(self.root)
        menu.title("Menu")

        tk.Label(menu, text="Select Field Size:").pack()
        tk.Button(menu, text="Small", command=lambda: self.start_game(menu, 200)).pack()
        tk.Button(menu, text="Medium", command=lambda: self.start_game(menu, 400)).pack()
        tk.Button(menu, text="Large", command=lambda: self.start_game(menu, 600)).pack()

        tk.Label(menu, text=f"Record: {self.record}").pack()
        tk.Button(menu, text="Exit", command=self.root.quit).pack()

    def start_game(self, menu, size):
        menu.destroy()
        self.canvas.config(width=size, height=size)
        self.root.update_idletasks()  # Обновляем интерфейс для корректного получения размеров канваса
        self.size = size // 20
        self.snake = [(size // 2, size // 2), (size // 2 - 20, size // 2), (size // 2 - 40, size // 2)]
        self.food = self.create_food()  # Создаем еду после обновления канваса
        self.direction = 'Right'
        self.game_over = False
        self.paused = False
        self.score = 0
        self.update_game()

    def create_food(self):
        # Получаем правильные размеры канваса после обновления интерфейса
        max_x = (self.canvas.winfo_width() // self.size) - 1
        max_y = (self.canvas.winfo_height() // self.size) - 1

        if max_x > 0 and max_y > 0:
            x = random.randint(0, max_x) * self.size
            y = random.randint(0, max_y) * self.size
            return x, y
        else:
            return 0, 0  # В случае ошибки возвращаем начальные координаты

    def change_direction(self, event):
        if event.keysym in ['Left', 'Right', 'Up', 'Down']:
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
            self.snake.append(self.snake[-1])  # удлиняем змейку
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
        self.paused = True
        stop_menu = tk.Toplevel(self.root)
        stop_menu.title("Pause Menu")
        tk.Label(stop_menu, text="Game Paused").pack()
        tk.Button(stop_menu, text="Continue", command=lambda: self.resume_game(stop_menu)).pack()
        tk.Button(stop_menu, text="Main Menu", command=lambda: self.back_to_menu(stop_menu)).pack()
        tk.Button(stop_menu, text="Exit", command=self.root.quit).pack()

    def resume_game(self, stop_menu):
        stop_menu.destroy()
        self.paused = False

    def back_to_menu(self, stop_menu):
        stop_menu.destroy()
        self.paused = False
        self.start_menu()

    def show_game_over_menu(self):
        game_over_menu = tk.Toplevel(self.root)
        game_over_menu.title("Game Over")
        tk.Label(game_over_menu, text="Game Over!").pack()
        tk.Label(game_over_menu, text=f"Score: {self.score}").pack()
        tk.Button(game_over_menu, text="Main Menu", command=lambda: self.back_to_menu(game_over_menu)).pack()
        tk.Button(game_over_menu, text="Exit", command=self.root.quit).pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    game.start_menu()
    root.mainloop()
