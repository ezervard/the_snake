import random
from random import choice, randint

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


# Тут опишите все классы игры.
class GameObject:
    def __init__(self):
        self.position = CENTER_POSITION
        self.body_color = DEFAULT_COLOR

    def draw(self):

        pass


class Apple(GameObject):
    def __init__(self) -> None:
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    @staticmethod
    def randomize_position():
        x_coord = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_coord = randint(0, GRID_HEIGHT  - 1) * GRID_SIZE
        #print(f'apple cords: {x_coord}, {y_coord}')
        return x_coord, y_coord

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    position = CENTER_POSITION

    def __init__(self):
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def get_head_position(self):
        return self.positions[0]

    def move(self):
        head_x, head_y = self.positions[0]

        if self.direction == RIGHT:
            head_x += GRID_SIZE
        elif self.direction == LEFT:
            head_x -= GRID_SIZE
        elif self.direction == UP:
            head_y -= GRID_SIZE
        elif self.direction == DOWN:
            head_y += GRID_SIZE
        new_head_position = (head_x, head_y)

        # Увеличение змейки
        if len(self.positions) < self.length:
            self.positions.insert(0, new_head_position)
        elif len(self.positions) == self.length and len(self.positions) != 1:
            self.positions[0] = new_head_position
            self.positions.pop(-1)
        else:
            self.positions[0] = new_head_position



    def reset(self):
        #реализовать метод перезапуска игры
        pass
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)


def handle_keys(game_object):
    for event in pygame.event.get():
        # print(event)
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


def main():
    pygame.init()
    apple = Apple()
    snake = Snake()
    run = True

    while run:
        clock.tick(SPEED)

        # Обновление состояния клавиатуры
        pygame.event.pump()
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        snake.move()
        snake.update_direction()
        #print(snake.positions[0])
        snake_x, snake_y = snake.positions[0]
        apple_x, apple_y = apple.position

        # Столкновение с яблоком
        snake_x , snake_y = snake.get_head_position()
        apple_x , apple_y = apple.position

        if snake_x - apple_x <= 5 and snake_y - apple_y <= 5:
            
            snake.length += 1
            apple.position = apple.randomize_position()
            print(snake.length)

        
        pygame.display.update()


if __name__ == '__main__':
    main()

# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
