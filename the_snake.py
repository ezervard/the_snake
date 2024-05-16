from random import randint, choice

import pygame

import placeholders as pl


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
BOARD_BACKGROUND_COLOR = (108, 156, 31)
BACKGROUND_IMG = pygame.image.load('images/background.png')
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (640, 490))

# Цвет границы ячеек
BORDER_COLOR = (93, 216, 228)

# Цвет по умолчанию
DEFAULT_COLOR = (100, 100, 100)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 30), 0, 32)

# Переменная состояний
STATE = "game_play"


# Игровые звуки
BACKGROUND_MUSIC = pygame.mixer.Sound('sounds/main_theme.mp3')
APPLE_SOUND = pygame.mixer.Sound('sounds/apple.mp3')
SELF_EAT_SOUND = pygame.mixer.Sound('sounds/self_eat.mp3')
CHOOSE_SOUND = pygame.mixer.Sound('sounds/key_sound.mp3')

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

    @staticmethod
    def draw_cell(position, body_color) -> None:
        """Метод для отрисовки ячейки"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод для переопределения в дочерних классах"""
        raise NotImplementedError


class Apple(GameObject):
    """Клас описывающий яблоко"""

    def __init__(self) -> None:
        """Инициализация яблока"""
        self.body_color = APPLE_COLOR
        self.image = pygame.image.load('images/apple.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.position = self.randomize_position()

    @staticmethod
    def randomize_position(snake_pos=CENTER_POSITION) -> tuple[int, int]:
        """Метод для случайной генерации позиции яблока
        с учётом позиции змейки.
        """
        while True:
            x_coord = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_coord = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x_coord, y_coord) in snake_pos:
                continue
            else:
                return x_coord, y_coord

    def draw(self) -> None:
        """Метод для отрисовки яблока"""
        screen.blit(self.image, self.position)


class Snake(GameObject):
    """Клас описывающий змейку"""

    position = CENTER_POSITION

    def __init__(self) -> None:
        """Инициализация змейки"""
        self.direction = DEFAULT_DIRECTION
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
        global STATE
        dx, dy = self.direction
        head_x, head_y = self.get_head_position()

        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT

        new_head_position = (new_head_x, new_head_y)

        if new_head_position in self.positions:
            self.reset()
            SELF_EAT_SOUND.play()
            STATE = 'game_over'

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
        if self.direction == RIGHT:
            self.head_rot = pygame.transform.rotate(self.head_rot, -90)
        elif self.direction == LEFT:
            self.head_rot = pygame.transform.rotate(self.head_rot, 90)
        elif self.direction == UP:
            self.head_rot = pygame.transform.rotate(self.head_rot, 0)
        else:
            self.head_rot = pygame.transform.rotate(self.head_rot, 180)

    def reset(self):
        """Метод для перезапуска игры"""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = DEFAULT_DIRECTION
        self.next_direction = None
        self.body_color = SNAKE_COLOR
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
                screen.blit(self.head_rot, position)
            elif i == len(self.positions) - 1:
                # Поворачиваем хвост
                dx = self.positions[-1][0] - self.positions[-2][0]
                dy = self.positions[-1][1] - self.positions[-2][1]
                angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))
                rotated_tail = pygame.transform.rotate(self.tail, angle)
                screen.blit(rotated_tail, position)
            else:
                screen.blit(self.image, position)


def handle_keys(game_object) -> None:
    """Функция для обработки нажатий клавиш"""
    global STATE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == pygame.KEYDOWN:
            handle_direction(event, game_object)
            handle_special_keys(event)


def handle_direction(event, game_object) -> None:
    """Метод описывающий изменение направления"""
    if event.key == pygame.K_UP and game_object.direction != DOWN:
        game_object.next_direction = UP
    elif event.key == pygame.K_DOWN and game_object.direction != UP:
        game_object.next_direction = DOWN
    elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
        game_object.next_direction = LEFT
    elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
        game_object.next_direction = RIGHT


def handle_special_keys(event) -> None:
    """Обработка специальных клавиш"""
    global STATE
    if event.key == pygame.K_ESCAPE:
        quit_game()
    elif event.key == pygame.K_SPACE:
        CHOOSE_SOUND.play()
        state_change()
    elif event.key == pygame.K_F1:
        if not ai.AI_STATE:
            ai.AI_STATE = True
        else:
            ai.AI_STATE = False


def quit_game() -> None:
    """Выход из игры"""
    pygame.quit()
    raise SystemExit


def state_change() -> None:
    """Изменение переменной состояния"""
    global STATE
    if STATE == "game_play":
        STATE = "game_pause"
    elif STATE == "game_pause":
        STATE = "game_play"
    elif STATE == "game_over":
        STATE = "game_play"


def main() -> None:
    """Основной цикл игры"""
    global SPEED
    pygame.init()
    apple = Apple()
    snake = Snake()
    BACKGROUND_MUSIC.set_volume(0.1)
    BACKGROUND_MUSIC.play()

    while True:
        if STATE == "game_play":
            clock.tick(SPEED)
            handle_keys(snake)
            screen.fill(BOARD_BACKGROUND_COLOR)
            screen.blit(BACKGROUND_IMG, (-3, -10))
            apple.draw()
            snake.draw()
            snake.move()
            snake.update_direction()
            pygame.draw.line(screen, (50, 56, 50), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 3)
            screen.blit(pl.score_text, (10, SCREEN_HEIGHT + 10))
            screen.blit(pl.info, (150, SCREEN_HEIGHT + 10))
            if snake.get_head_position() == apple.position:
                snake.length += 1
                score = snake.length - 1
                SPEED += 0.1
                apple.position = apple.randomize_position(snake.positions)
                APPLE_SOUND.set_volume(300)
                APPLE_SOUND.play()
                pl.score_text = pl.score_font.render(f"Score: {score}", True, pygame.color.Color('White'))
                pl.loose_score = pl.loose_font.render(f"You Score: {score}", True, pygame.color.Color(pl.RED_CLR))
            pygame.display.update()
        elif STATE == "game_pause":
            handle_keys(snake)
            screen.blit(pl.pause_text, (280, 180))
            screen.blit(pl.pause_info, (220, 230))
            pygame.display.update()
        elif STATE == "game_over":
            handle_keys(snake)
            screen.blit(pl.loose_text, (260, 180))
            screen.blit(pl.loose_info, (225, 230))
            screen.blit(pl.loose_score, (260, 280))
            pygame.display.update()


if __name__ == '__main__':
    main()
