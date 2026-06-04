import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
DELAY = 120

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="black",
        )
        self.canvas.pack()

        self.reset_game()
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<space>", lambda event: self.reset_game())

        self.running = True
        self.game_loop()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = "Right"
        self.score = 0
        self.place_food()
        self.draw()

    def place_food(self):
        empty_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake
        ]
        self.food = random.choice(empty_cells)

    def change_direction(self, new_direction):
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if opposite[new_direction] != self.direction:
            self.direction = new_direction

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1

        new_head = (head_x, head_y)

        if self.check_collision(new_head):
            self.running = False
            self.show_game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

    def check_collision(self, position):
        x, y = position
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True
        if position in self.snake:
            return True
        return False

    def draw(self):
        self.canvas.delete("all")
        for x, y in self.snake:
            self.draw_cell(x, y, "lime")
        self.draw_cell(*self.food, "red")
        self.canvas.create_text(
            60,
            10,
            text=f"Score: {self.score}",
            fill="white",
            anchor="nw",
            font=("Arial", 12, "bold"),
        )

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222")

    def show_game_over(self):
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2,
            GRID_HEIGHT * CELL_SIZE // 2,
            text=f"Game Over\nScore: {self.score}\nPress Space to restart",
            fill="white",
            font=("Arial", 16, "bold"),
            justify="center",
        )

    def game_loop(self):
        if self.running:
            self.move_snake()
            self.draw()
        self.root.after(DELAY, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
