import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
DELAY = 120

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}
OPPOSITE = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

class Snake:
    def __init__(self, body, direction, color, name):
        self.body = body
        self.direction = direction
        self.next_direction = direction
        self.color = color
        self.name = name
        self.score = 0
        self.alive = True

    @property
    def head(self):
        return self.body[0]

    def set_direction(self, new_direction):
        if self.alive and OPPOSITE[new_direction] != self.direction:
            self.next_direction = new_direction

    def next_head(self):
        dx, dy = DIRECTIONS[self.next_direction]
        x, y = self.head
        return x + dx, y + dy

    def move(self, grow=False):
        self.direction = self.next_direction
        new_head = self.next_head()
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()
        return new_head

    def occupies(self, position):
        return position in self.body

    def reset(self, body, direction):
        self.body = body
        self.direction = direction
        self.next_direction = direction
        self.score = 0
        self.alive = True

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake vs AI")
        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="black",
        )
        self.canvas.pack()

        self.human = Snake([(5, GRID_HEIGHT // 2), (4, GRID_HEIGHT // 2), (3, GRID_HEIGHT // 2)], "Right", "lime", "Human")
        self.ai = Snake([(GRID_WIDTH - 6, GRID_HEIGHT // 2), (GRID_WIDTH - 5, GRID_HEIGHT // 2), (GRID_WIDTH - 4, GRID_HEIGHT // 2)], "Left", "cyan", "AI")

        self.root.bind("<Up>", lambda event: self.human.set_direction("Up"))
        self.root.bind("<Down>", lambda event: self.human.set_direction("Down"))
        self.root.bind("<Left>", lambda event: self.human.set_direction("Left"))
        self.root.bind("<Right>", lambda event: self.human.set_direction("Right"))
        self.root.bind("<space>", lambda event: self.reset_game())
        self.root.bind("r", lambda event: self.reset_game())

        self.place_food()
        self.running = True
        self.game_loop()

    def reset_game(self):
        self.human.reset([(5, GRID_HEIGHT // 2), (4, GRID_HEIGHT // 2), (3, GRID_HEIGHT // 2)], "Right")
        self.ai.reset([(GRID_WIDTH - 6, GRID_HEIGHT // 2), (GRID_WIDTH - 5, GRID_HEIGHT // 2), (GRID_WIDTH - 4, GRID_HEIGHT // 2)], "Left")
        self.place_food()
        self.running = True
        self.draw()

    def place_food(self):
        occupied = set(self.human.body) | set(self.ai.body)
        empty_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        self.food = random.choice(empty_cells)

    def ai_decide(self):
        if not self.ai.alive:
            return

        priorities = sorted(DIRECTIONS.keys(), key=lambda d: self.manhattan_distance(self.destination_after(self.ai, d), self.food))
        for direction in priorities:
            if OPPOSITE[direction] == self.ai.direction:
                continue
            head = self.destination_after(self.ai, direction)
            if self.is_safe_position(head, self.ai):
                self.ai.next_direction = direction
                return

        for direction in DIRECTIONS:
            if OPPOSITE[direction] == self.ai.direction:
                continue
            head = self.destination_after(self.ai, direction)
            if self.is_safe_position(head, self.ai):
                self.ai.next_direction = direction
                return

    def destination_after(self, snake, direction):
        dx, dy = DIRECTIONS[direction]
        x, y = snake.head
        return x + dx, y + dy

    def is_safe_position(self, position, snake):
        x, y = position
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False

        occupied = set(self.human.body) | set(self.ai.body)
        if position in occupied and position != snake.body[-1]:
            return False

        if position in snake.body[:-1]:
            return False

        return True

    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def game_loop(self):
        if self.running:
            self.ai_decide()
            self.update_snakes()
            self.draw()
        self.root.after(DELAY, self.game_loop)

    def update_snakes(self):
        human_next = self.human.next_head() if self.human.alive else None
        ai_next = self.ai.next_head() if self.ai.alive else None

        human_crash = self.detect_crash(self.human, human_next, self.ai, ai_next)
        ai_crash = self.detect_crash(self.ai, ai_next, self.human, human_next)

        if human_crash and ai_crash:
            self.human.alive = False
            self.ai.alive = False
            self.running = False
            return

        if human_crash:
            self.human.alive = False
            self.running = False
        if ai_crash:
            self.ai.alive = False

        human_grow = self.human.alive and human_next == self.food
        ai_grow = self.ai.alive and ai_next == self.food

        if human_grow:
            self.human.score += 1
        if ai_grow:
            self.ai.score += 1

        if self.human.alive:
            self.human.move(grow=human_grow)
        if self.ai.alive:
            self.ai.move(grow=ai_grow)

        if human_grow or ai_grow:
            self.place_food()

        if not self.human.alive and not self.ai.alive:
            self.running = False

    def detect_crash(self, snake, next_head, other_snake, other_next_head):
        if next_head is None:
            return False

        x, y = next_head
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True

        if next_head in snake.body[:-1]:
            return True

        other_occupied = set(other_snake.body)
        if next_head in other_occupied and next_head != other_snake.body[-1]:
            return True

        if next_head == other_next_head:
            return True

        if next_head == other_snake.head and other_next_head == snake.head:
            return True

        return False

    def draw(self):
        self.canvas.delete("all")
        self.draw_cell(*self.food, "red")
        for x, y in self.human.body:
            self.draw_cell(x, y, self.human.color)
        for x, y in self.ai.body:
            self.draw_cell(x, y, self.ai.color)

        status = f"Human: {self.human.score}   AI: {self.ai.score}"
        self.canvas.create_text(
            10,
            10,
            text=status,
            fill="white",
            anchor="nw",
            font=("Arial", 12, "bold"),
        )

        if not self.running:
            result_text = self.game_over_text()
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2,
                GRID_HEIGHT * CELL_SIZE // 2,
                text=result_text,
                fill="white",
                font=("Arial", 16, "bold"),
                justify="center",
            )

    def game_over_text(self):
        if self.human.score > self.ai.score:
            winner = "Human wins!"
        elif self.ai.score > self.human.score:
            winner = "AI wins!"
        else:
            winner = "Draw!"
        return f"Game Over\n{winner}\nHuman: {self.human.score}  AI: {self.ai.score}\nPress Space or R to restart"

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222")

if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
