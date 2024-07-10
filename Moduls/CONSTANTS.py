import pygame
from random import choice
import os, sys

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

resource_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

background_path = os.path.join(resource_path, '../images/background.png')
apple_path = os.path.join(resource_path, '../images/apple.png')
snake_body_path = os.path.join(resource_path, '../images/snake_body.png')
snake_head_path = os.path.join(resource_path, '../images/snake_head.png')
snake_tail_path = os.path.join(resource_path, '../images/snake_tail.png')
apple_sound_path = os.path.join(resource_path, '../sounds/apple.mp3')
key_sound_path = os.path.join(resource_path, '../sounds/key_sound.mp3')

# Цвет фона:
BOARD_BACKGROUND_COLOR = (108, 156, 31)
BACKGROUND_IMG = pygame.image.load(background_path)
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (640, 490))

APPLE_IMG = pygame.image.load(apple_path)
SNAKE_BODY_IMG = pygame.image.load(snake_body_path)
SNAKE_HEAD_IMG = pygame.image.load(snake_head_path)
SNAKE_TAIL_IMG = pygame.image.load(snake_tail_path)
# Игровые звуки
#BACKGROUND_MUSIC = pygame.mixer.Sound('../sounds/main_theme.mp3')
APPLE_SOUND = pygame.mixer.Sound(apple_sound_path)
#SELF_EAT_SOUND = pygame.mixer.Sound('../sounds/self_eat.mp3')
CHOOSE_SOUND = pygame.mixer.Sound(key_sound_path)

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
