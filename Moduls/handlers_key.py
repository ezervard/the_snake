import pygame

from Moduls import CONSTANTS as ct


def handle_keys(game_object) -> None:
    """Функция для обработки нажатий клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == pygame.KEYDOWN:
            handle_direction(event, game_object)
            handle_special_keys(event)


def handle_direction(event, game_object) -> None:
    """Метод описывающий изменение направления"""
    if event.key == pygame.K_UP and game_object.direction != ct.DOWN:
        game_object.next_direction = ct.UP
    elif event.key == pygame.K_DOWN and game_object.direction != ct.UP:
        game_object.next_direction = ct.DOWN
    elif event.key == pygame.K_LEFT and game_object.direction != ct.RIGHT:
        game_object.next_direction = ct.LEFT
    elif event.key == pygame.K_RIGHT and game_object.direction != ct.LEFT:
        game_object.next_direction = ct.RIGHT


def handle_special_keys(event) -> None:
    """Обработка специальных клавиш"""
    if event.key == pygame.K_ESCAPE:
        quit_game()
    elif event.key == pygame.K_SPACE:
        ct.CHOOSE_SOUND.play()
        state_change()


def quit_game() -> None:
    """Выход из игры"""
    pygame.quit()
    raise SystemExit


def state_change() -> None:
    """Изменение переменной состояния"""
    if ct.STATE == "game_play":
        ct.STATE = "game_pause"
    elif ct.STATE == "game_pause":
        ct.STATE = "game_play"
    elif ct.STATE == "game_over":
        ct.STATE = "game_play"
