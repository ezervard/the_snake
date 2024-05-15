import the_snake
import numpy as np

AI_STATE = False
REWARDS = 0

def check_ai(func):
    """Декоратор отключения управления игрока"""
    def wrapper(*args, **kwargs):
        if not AI_STATE:
            return func(*args, **kwargs)
    return wrapper





def move(direction, GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT) -> None:
    """Метод описывающий движение змейки по игровому полю"""
    global STATE
    dx, dy = direction
    head_x, head_y = get_head_position()

    new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
    new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT

    new_head_position = (new_head_x, new_head_y)

    if new_head_position in self.positions:
        self.reset()
        REWARDS = - 10
        SELF_EAT_SOUND.play()
        STATE = 'game_over'

    self.positions.insert(0, new_head_position)

    if len(self.positions) > self.length:
        self.positions.pop()

    # Поворачиваем голову змеи только если есть новое направление
    self.update_direction()
    if self.direction != self.next_direction:
        self.rotate_head()


def ai_move(func):
    def wrapper(*args, **kwargs):
        if AI_STATE:
            dir = args[0]  # Получаем текущее направление змейки
            clock_wise = [the_snake.RIGHT, the_snake.DOWN, the_snake.LEFT, the_snake.UP]
            idx = clock_wise.index(dir)
            if np.array_equal(args, [1, 0, 0]):
                new_dir = clock_wise[idx]
            elif np.array_equal(args, [0, 1, 0]):
                next_dir = (idx + 1) % 4
                new_dir = clock_wise[next_dir]
            else:
                next_dir = (idx - 1) % 4
                new_dir = clock_wise[next_dir]
            return new_dir
        else:
            return func(*args, **kwargs)
    return wrapper


