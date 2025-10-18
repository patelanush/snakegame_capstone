import pygame, random, sys

CELL_SIZE = 25
GRID_W, GRID_H = 24, 24
WIDTH, HEIGHT = GRID_W * CELL_SIZE, GRID_H * CELL_SIZE
FPS = 12
BG = (18, 18, 18)
SNAKE = (60, 300, 85)
SNAKE_HEAD = (90, 230, 125)
APPLE = (220, 70, 70)
GRID = (35, 35, 35)
TEXT = (230, 230, 270)
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

def draw_cell(surface, x, y, color):
    r = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, r, border_radius=6)

def random_empty_cell(occupied):
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if pos not in occupied:
            return pos

def draw_grid(surface):
    for x in range(GRID_W):
        pygame.draw.line(surface, GRID, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(GRID_H):
        pygame.draw.line(surface, GRID, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))

def show_center_text(surface, lines, font):
    total_h = sum(font.size(t)[1] for t in lines) + (len(lines) - 1) * 8
    y = HEIGHT // 2 - total_h // 2
    for t in lines:
        s = font.render(t, True, TEXT)
        x = WIDTH // 2 - s.get_width() // 2
        surface.blit(s, (x, y))
        y += s.get_height() + 8

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_dir = RIGHT
        self.apple = random_empty_cell(set(self.snake))
        self.score = 0
        self.game_over = False
        self.paused = False

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key in (pygame.K_UP, pygame.K_w):
                self.set_dir(UP)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.set_dir(DOWN)
            elif key in (pygame.K_LEFT, pygame.K_a):
                self.set_dir(LEFT)
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.set_dir(RIGHT)
            elif key == pygame.K_p:
                self.paused = not self.paused
            elif key == pygame.K_r:
                self.reset()
            elif key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.quit()
                sys.exit()

    def set_dir(self, d):
        if d != OPPOSITE.get(self.direction):
            self.next_dir = d

    def step(self):
        if self.game_over or self.paused:
            return
        self.direction = self.next_dir
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_W, (head_y + dy) % GRID_H)
        if new_head in self.snake:
            self.game_over = True
            return
        self.snake.insert(0, new_head)
        if new_head == self.apple:
            self.score += 1
            self.apple = random_empty_cell(set(self.snake))
        else:
            self.snake.pop()

    def draw(self, surface, font):
        surface.fill(BG)
        draw_grid(surface)
        draw_cell(surface, *self.apple, APPLE)
        for i, (x, y) in enumerate(self.snake):
            color = SNAKE_HEAD if i == 0 else SNAKE
            draw_cell(surface, x, y, color)
        score_surf = font.render(f"Score: {self.score}", True, TEXT)
        surface.blit(score_surf, (10, 8))
        if self.paused:
            show_center_text(surface, ["Paused", "Press P to resume"], font)
        if self.game_over:
            show_center_text(surface, [f"Game Over - Score {self.score}", "Press R to restart"], font)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24, bold=True)
    game = SnakeGame()
    while True:
        speed = min(FPS + game.score // 5, 24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_input(event)
        game.step() 
        game.draw(screen, font)
        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    main()
