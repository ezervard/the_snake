from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = SCREEN_WIDTH // 2 - GRID_SIZE, SCREEN_HEIGHT // 2 - GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
DEFAULT_DIRECTION = choice(DIRECTIONS)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

DEFAULT_COLOR = (100, 100, 100)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self) -> None:
        """Инициализация объекта игры."""
        self.position = CENTER_POSITION
        self.body_color = DEFAULT_COLOR

    def draw(self) -> None:
        """Метод для переопределения в дочерних класах"""
        pass


class Apple(GameObject):
    """Клас описывающий яблоко"""

    def __init__(self) -> None:
        """Инициализация яблока"""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    @staticmethod
    def randomize_position() -> tuple[int, int]:
        """метод для случайной генерации позиции яблока"""
        x_coord = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_coord = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x_coord, y_coord

    def draw(self) -> None:
        """метод для отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Клас описывающий змейку"""

    position = CENTER_POSITION

    def __init__(self) -> None:
        """инициализация змейки"""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.body_color = SNAKE_COLOR
        self.direction = DEFAULT_DIRECTION
        self.next_direction = None

    def update_direction(self) -> None:
        """метод для изменения направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple[int, int]:
        """Метод для получения позиции голловы змейки"""
        return self.positions[0]

    def move(self) -> None:
        """метод описывающий движение змейки по игровому полю"""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction

        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT

        new_head_position = (new_head_x, new_head_y)

        if new_head_position in self.positions:
            self.reset()

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.positions.pop()

    # Метод для сброса змейки
    def reset(self):
        """Метод для перезапуска игры"""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = DEFAULT_DIRECTION
        self.next_direction = None

    def draw(self):
        """метод для отрисовки змейки"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object) -> None:
    """Функция для обработки нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры"""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        snake.move()
        snake.update_direction()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
