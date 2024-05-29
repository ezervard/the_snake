from random import randint

import pygame

from moduls import CONSTANTS as ct, handlers_key as hd, placeholders as pl


class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self) -> None:
        """Инициализация объекта игры."""
        self.position = ct.CENTER_POSITION
        self.body_color = ct.DEFAULT_COLOR

    @staticmethod
    def draw_cell(position, body_color) -> None:
        """Метод для отрисовки ячейки"""
        rect = pygame.Rect(position, (ct.GRID_SIZE, ct.GRID_SIZE))
        pygame.draw.rect(ct.screen, body_color, rect)
        pygame.draw.rect(ct.screen, ct.BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод для переопределения в дочерних классах"""
        raise NotImplementedError


class Apple(GameObject):
    """Клас описывающий яблоко"""

    def __init__(self) -> None:
        """Инициализация яблока"""
        super().__init__()
        self.body_color = ct.APPLE_COLOR
        self.image = pygame.image.load('images/apple.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.position = self.randomize_position()

    @staticmethod
    def randomize_position(snake_pos=ct.CENTER_POSITION) -> tuple[int, int]:
        """Метод для случайной генерации позиции яблока
        с учётом позиции змейки.
        """
        while True:
            x_coord = randint(0, ct.GRID_WIDTH - 1) * ct.GRID_SIZE
            y_coord = randint(0, ct.GRID_HEIGHT - 1) * ct.GRID_SIZE
            if (x_coord, y_coord) in snake_pos:
                continue
            else:
                return x_coord, y_coord

    def draw(self) -> None:
        """Метод для отрисовки яблока"""
        ct.screen.blit(self.image, self.position)


class Snake(GameObject):
    """Клас описывающий змейку"""

    position = ct.CENTER_POSITION

    def __init__(self) -> None:
        """Инициализация змейки"""
        super().__init__()
        self.positions = None
        self.length = 1
        self.tail = None
        self.head_rot = None
        self.head = None
        self.image = None
        self.next_direction = None
        self.direction = ct.DEFAULT_DIRECTION
        self.reset()

    def update_direction(self) -> None:
        """Метод для изменения направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple[int, int]:
        """Метод для получения позиции головы змейки"""
        return self.positions[0]

    def move(self) -> None:
        """Метод описывающий движение змейки по игровому полю"""

        dx, dy = self.direction
        head_x, head_y = self.get_head_position()

        new_head_x = (head_x + dx * ct.GRID_SIZE) % ct.SCREEN_WIDTH
        new_head_y = (head_y + dy * ct.GRID_SIZE) % ct.SCREEN_HEIGHT

        new_head_position = (new_head_x, new_head_y)

        if new_head_position in self.positions:
            self.reset()
            ct.SELF_EAT_SOUND.play()
            ct.STATE = 'game_over'

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.positions.pop()

        # Поворачиваем голову змеи только если есть новое направление
        self.update_direction()
        if self.direction != self.next_direction:
            self.rotate_head()

    def rotate_head(self) -> None:
        """Метод поворота головы"""
        self.head_rot = self.head
        if self.direction == ct.RIGHT:
            self.head_rot = pygame.transform.rotate(self.head_rot, -90)
        elif self.direction == ct.LEFT:
            self.head_rot = pygame.transform.rotate(self.head_rot, 90)
        elif self.direction == ct.UP:
            self.head_rot = pygame.transform.rotate(self.head_rot, 0)
        else:
            self.head_rot = pygame.transform.rotate(self.head_rot, 180)

    def reset(self):
        """Метод для перезапуска игры"""
        self.length = 1
        self.positions = [ct.CENTER_POSITION]
        self.direction = ct.DEFAULT_DIRECTION
        self.next_direction = None
        self.body_color = ct.SNAKE_COLOR
        self.image = pygame.image.load('images/snake_body.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.head = pygame.image.load('images/snake_head.png')
        self.head = pygame.transform.scale(self.head, (20, 20))
        self.tail = pygame.image.load('images/snake_tail.png')
        self.tail = pygame.transform.scale(self.tail, (20, 20))
        self.tail = pygame.transform.rotate(self.tail, 90)
        self.head_rot = self.head

    def draw(self):
        """Метод для отрисовки змейки"""
        for i, position in enumerate(self.positions):
            if position == self.get_head_position():
                ct.screen.blit(self.head_rot, position)
            elif i == len(self.positions) - 1:
                dx = self.positions[-1][0] - self.positions[-2][0]
                dy = self.positions[-1][1] - self.positions[-2][1]
                angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))
                rotated_tail = pygame.transform.rotate(self.tail, angle)
                ct.screen.blit(rotated_tail, position)
            else:
                ct.screen.blit(self.image, position)


def main() -> None:
    """Основной цикл игры"""
    pygame.init()
    apple = Apple()
    snake = Snake()
    ct.BACKGROUND_MUSIC.set_volume(0.1)
    ct.BACKGROUND_MUSIC.play()

    while True:
        if ct.STATE == "game_play":
            ct.clock.tick(ct.SPEED)
            hd.handle_keys(snake)
            ct.screen.fill(ct.BOARD_BACKGROUND_COLOR)
            ct.screen.blit(ct.BACKGROUND_IMG, (-3, -10))
            apple.draw()
            snake.draw()
            snake.move()
            snake.update_direction()
            pygame.draw.line(ct.screen, (50, 56, 50), (0, ct.SCREEN_HEIGHT), (ct.SCREEN_WIDTH, ct.SCREEN_HEIGHT), 3)
            ct.screen.blit(pl.score_text, (10, ct.SCREEN_HEIGHT + 10))
            ct.screen.blit(pl.info, (150, ct.SCREEN_HEIGHT + 10))
            if snake.get_head_position() == apple.position:
                snake.length += 1
                score = snake.length - 1
                ct.SPEED += 0.1
                apple.position = apple.randomize_position(snake.positions)
                ct.APPLE_SOUND.set_volume(300)
                ct.APPLE_SOUND.play()
                pl.score_text = pl.score_font.render(f"Score: {score}", True, pygame.color.Color('White'))
                pl.loose_score = pl.loose_font.render(f"You Score: {score}", True, pygame.color.Color(pl.RED_CLR))
            pygame.display.update()
        elif ct.STATE == "game_pause":
            hd.handle_keys(snake)
            ct.screen.blit(pl.pause_text, (280, 180))
            ct.screen.blit(pl.pause_info, (220, 230))
            pygame.display.update()
        elif ct.STATE == "game_over":
            hd.handle_keys(snake)
            ct.screen.blit(pl.loose_text, (260, 180))
            ct.screen.blit(pl.loose_info, (225, 230))
            ct.screen.blit(pl.loose_score, (260, 280))
            pygame.display.update()


if __name__ == '__main__':
    main()

