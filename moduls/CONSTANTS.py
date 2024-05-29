import pygame
from random import choice


pygame.init()

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

# Цвет фона:
BOARD_BACKGROUND_COLOR = (108, 156, 31)
BACKGROUND_IMG = pygame.image.load('./images/background.png')
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (640, 490))

# Игровые звуки
BACKGROUND_MUSIC = pygame.mixer.Sound('./sounds/main_theme.mp3')
APPLE_SOUND = pygame.mixer.Sound('./sounds/apple.mp3')
SELF_EAT_SOUND = pygame.mixer.Sound('./sounds/self_eat.mp3')
CHOOSE_SOUND = pygame.mixer.Sound('./sounds/key_sound.mp3')

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 30))

# Переменная состояний
STATE = "game_play"

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()
