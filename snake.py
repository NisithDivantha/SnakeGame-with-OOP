import pygame
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 20
SPECIAL_FOOD_SIZE = CELL_SIZE * 2  # Special food is larger

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Color for special food

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Food:
    def __init__(self, position, size=CELL_SIZE, color=RED):
        self.position = position
        self.size = size
        self.color = color

    def effect(self, game):
        game.snake.grow()

class SpecialFood(Food):
    def __init__(self, position):
        super().__init__(position, size=SPECIAL_FOOD_SIZE, color=BLUE)

    def effect(self, game):
        super().effect(game)
        game.score += 10

class Snake:
    def __init__(self, initial_position):
        self.segments = [initial_position]
        self.direction = Position(1, 0)
        self.grow_next_move = False

    def move(self):
        head = self.segments[0]
        new_head = Position(head.x + self.direction.x, head.y + self.direction.y)
        self.segments.insert(0, new_head)

        if self.grow_next_move:
            self.grow_next_move = False
        else:
            self.segments.pop()

    def grow(self):
        self.grow_next_move = True

    def set_direction(self, direction):
        if (self.direction.x + direction.x != 0 or self.direction.y + direction.y != 0):
            self.direction = direction

class Game:
    def __init__(self):
        self.snake = Snake(Position(5, 5))
        self.score = 0
        self.game_over = False
        self.food = self.generate_food()

    def generate_food(self):
        while True:
            food_position = Position(random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                                     random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))
            if food_position not in self.snake.segments:
                if self.score > 0 and self.score % 5 == 0:
                    return SpecialFood(food_position)
                else:
                    return Food(food_position)

    def update(self):
        self.snake.move()
        if self.check_collision_with_food():
            self.food.effect(self)
            self.food = self.generate_food()
            self.score += 1

        if self.check_collision_with_self() or self.check_collision_with_boundaries():
            self.game_over = True

    def check_collision_with_food(self):
        head = self.snake.segments[0]
        return head == self.food.position

    def check_collision_with_self(self):
        head = self.snake.segments[0]
        return any(segment == head for segment in self.snake.segments[1:])

    def check_collision_with_boundaries(self):
        head = self.snake.segments[0]
        return head.x < 0 or head.x >= SCREEN_WIDTH // CELL_SIZE or head.y < 0 or head.y >= SCREEN_HEIGHT // CELL_SIZE

    def render(self, screen):
        screen.fill(BLACK)
        for segment in self.snake.segments:
            pygame.draw.rect(screen, GREEN, (segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, self.food.color, (self.food.position.x * CELL_SIZE, self.food.position.y * CELL_SIZE, self.food.size, self.food.size))
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(text, (10, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game.snake.set_direction(Position(0, -1))
                elif event.key == pygame.K_s:
                    game.snake.set_direction(Position(0, 1))
                elif event.key == pygame.K_a:
                    game.snake.set_direction(Position(-1, 0))
                elif event.key == pygame.K_d:
                    game.snake.set_direction(Position(1, 0))

        if not game.game_over:
            game.update()
            game.render(screen)
            pygame.display.flip()
            clock.tick(10)
        else:
            # Display "Game Over" message and score
            screen.fill(BLACK)
            font_large = pygame.font.Font(None, 72)
            font_small = pygame.font.Font(None, 36)
            text_game_over = font_large.render('Game Over', True, RED)
            text_score = font_small.render(f'Score: {game.score}', True, WHITE)
            screen.blit(text_game_over, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 36))
            screen.blit(text_score, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 36))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    pygame.quit()

if __name__ == '__main__':
    main()
